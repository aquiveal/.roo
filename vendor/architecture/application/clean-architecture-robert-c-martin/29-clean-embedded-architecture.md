# @Domain
This rule set is activated when the AI is writing, refactoring, or reviewing code for embedded systems, Internet of Things (IoT) devices, firmware, C/C++ hardware-interfacing applications, Real-Time Operating System (RTOS) integrations, or any software system that interacts directly with physical hardware or specialized microprocessors.

# @Vocabulary
- **Software**: The domain/business logic of the application. It has a long useful life and must be entirely independent of the underlying hardware, OS, or processor.
- **Firmware**: Code that interacts directly with the hardware or processor. It is firm because it is bound to the silicon and becomes obsolete as hardware evolves.
- **App-titude Test**: The anti-pattern where a programmer stops working as soon as the code "works" (passes the test of executing correctly), without refactoring to make the structure "right".
- **Target-Hardware Bottleneck**: A severe developmental slowdown caused by code being so tightly coupled to the hardware that it can *only* be tested on the physical target device.
- **HAL (Hardware Abstraction Layer)**: An interface boundary separating the Software from the Firmware. It defines services based on the *application's needs*, not the hardware's capabilities.
- **PAL (Processor Abstraction Layer)**: A boundary that isolates processor-specific C language extensions, special registers, and specific micro-controller peripherals from the rest of the codebase.
- **OSAL (Operating System Abstraction Layer)**: A layer separating the Software from the specific Operating System or RTOS, preventing semantic and syntactic lock-in to a specific vendor.

# @Objectives
- **Eliminate the Target-Hardware Bottleneck**: The AI must ensure that all Software (domain logic) can be compiled and tested off-target (e.g., on a standard x86/x64 development machine).
- **Enforce Separation of Concerns**: The AI must strictly separate domain logic from hardware setup, peripheral communication, and OS primitives.
- **Maximize Code Lifespan**: The AI must prevent unmanaged dependencies on hardware, firmware, or toolchains from destroying the software from within.
- **Design for Substitutability**: The AI must establish seams and substitution points (interfaces) to facilitate testability and future hardware migrations.

# @Guidelines

## General Embedded Architecture Constraints
- The AI MUST NOT stop at "Make it work." The AI MUST fulfill Kent Beck's software progression: 1. "Make it work", 2. "Make it right" (Refactor for clean architecture), 3. "Make it fast" (Refactor for performance only where necessary).
- The AI MUST NOT intermingle domain logic functions with hardware setup functions, hardware reaction functions (e.g., raw button handlers), or storage functions in the same file or module.

## Hardware Abstraction Layer (HAL) Rules
- The AI MUST design the HAL API from the perspective of the application's domain needs, NOT the hardware's capabilities.
- The AI MUST hide the underlying implementation details (e.g., flash memory, spinning disk, cloud) entirely behind the HAL. The user of the HAL MUST NOT know how the hardware achieves the result.

## Processor and Toolchain Abstraction (PAL) Rules
- The AI MUST NOT use vendor-supplied C compiler extensions (e.g., non-standard keywords, binary literals like `0b11000000`, or global hardware register variables like `SBUF0`, `TI_0`) in the Software layer.
- The AI MUST confine all processor-specific language extensions and register accesses to the Firmware layer, explicitly behind a PAL.
- The AI MUST use standardized types (e.g., `stdint.h` types like `uint32_t`) rather than vendor-specific types (e.g., `Uint_32`).
- If the target compiler does not provide `stdint.h`, the AI MUST generate a custom `stdint.h` that maps standard types to the vendor's types, thereby keeping the rest of the codebase clean and portable.

## Operating System Abstraction (OSAL) Rules
- The AI MUST NOT allow the Software layer to call RTOS or OS API functions directly.
- The AI MUST wrap all OS concurrency models, message passing, and threading primitives inside an OSAL.
- The AI MUST use the OSAL to establish test points so that application code can be tested off-OS.

## Interface and Header File Strictness
- The AI MUST use header files strictly as interface definitions.
- The AI MUST limit header files to function declarations, constants, and struct names *strictly necessary* to use the interface.
- The AI MUST NOT clutter header files with implementation details, private data structures, private constants, or typedefs that are only used internally by the `.c` / `.cpp` implementation file.

## DRY Conditional Compilation
- The AI MUST NOT use repeated conditional compilation directives (e.g., `#ifdef BOARD_V2`) scattered throughout the codebase to handle different targets.
- The AI MUST handle hardware variations by providing different implementations of HAL interfaces and binding them using the linker or runtime mechanisms, keeping the business logic free of `#ifdef`.

# @Workflow
When generating or refactoring embedded code, the AI MUST follow this exact sequence:
1. **Analyze and Separate**: Identify and categorize all required functions into Domain Logic, Hardware Setup, IO Reading/Writing, and OS/Threading primitives.
2. **Define the Seams (Interfaces)**: Draft header files for the HAL, PAL, and OSAL. Ensure function names reflect business/domain intent, not hardware mechanics. Ensure headers contain zero implementation details.
3. **Implement Firmware/Mechanics**: Write the `.c`/`.cpp` files that implement the HAL/PAL/OSAL interfaces using the vendor-specific registers, RTOS calls, and C-extensions.
4. **Implement Software (Domain Logic)**: Write the core business logic utilizing ONLY the standard C/C++ libraries and the defined HAL/OSAL interfaces. Ensure this code can compile cleanly on a non-embedded host machine.
5. **Establish Substitutability**: Create test-doubles (stubs/mocks) for the HAL/OSAL to prove the domain logic can be unit-tested off-target.
6. **Link and Bind**: Configure the build system (or instructions) to link the hardware-specific implementations for the target build, and the test-doubles for the local test build, avoiding `#ifdef` pollution.

# @Examples (Do's and Don'ts)

## HAL Interface Naming
- **[DO]**: `void Indicate_LowBattery(void);` (Abstracts the hardware, expresses the application's intent).
- **[DON'T]**: `void Led_TurnOn(int pin);` (Exposes the hardware mechanics to the software layer).

## Processor Dependencies and Types
- **[DO]**: 
  ```c
  #include <stdint.h>
  
  void calculate_rpm(uint32_t raw_sensor_value);
  ```
- **[DON'T]**: 
  ```c
  #include <acmetypes.h>
  
  void calculate_rpm(Uint_32 raw_sensor_value);
  ```

## Hardware Register Access
- **[DO]**: 
  Isolate register access in a dedicated firmware file (`serial_pal.c`) behind an interface:
  ```c
  #include "serial_pal.h"
  // Inside serial_pal.c
  void PAL_Serial_SendChar(char c) {
      SBUF0 = c;
      while(TI_0 == 0);
      TI_0 = 0;
  }
  ```
- **[DON'T]**: 
  Mix business logic with raw registers in the main application:
  ```c
  void say_hi() {
      IE = 0b11000000;
      SBUF0 = 'h';
      while(TI_0 == 0);
      // ...
  }
  ```

## Header File Clutter
- **[DO]**: 
  ```c
  // sensor_hal.h
  #ifndef SENSOR_HAL_H
  #define SENSOR_HAL_H
  
  float Sensor_GetTemperature(void);
  
  #endif
  ```
- **[DON'T]**: 
  ```c
  // sensor_hal.h
  #ifndef SENSOR_HAL_H
  #define SENSOR_HAL_H
  
  // Implementation details leaking into the interface!
  #define I2C_ADDR 0x48
  typedef struct { int raw_val; int offset; } InternalSensorState;
  InternalSensorState state; 
  
  float Sensor_GetTemperature(void);
  
  #endif
  ```

## DRY Conditional Compilation
- **[DO]**: 
  Write one clean software file `processor.c` that calls `HAL_Init()`. Compile `hal_board_v1.c` for Board 1, and `hal_board_v2.c` for Board 2 using the build system (Makefile/CMake).
- **[DON'T]**: 
  ```c
  void initialize_system() {
  #ifdef BOARD_V1
      init_legacy_hardware();
  #elif defined(BOARD_V2)
      init_new_hardware();
  #endif
  }
  ```