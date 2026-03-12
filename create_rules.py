import argparse
import os
import sys
import re
import asyncio
import aiohttp

WEBHOOK_URL_1 = "https://n8n.capybaara.com/webhook/24754bad-0c9c-4abf-b2aa-138547fe05b9"
WEBHOOK_URL_2 = "https://n8n.capybaara.com/webhook/88829b1c-e926-48ce-887d-b0d5805e6557"

def slugify(text):
    text = str(text).lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

async def get_chapters(session, book_title, content):
    payload_1 = {
        "book": {
            "metadata": {
                "title": book_title
            },
            "content": content
        }
    }

    print(f"Sending first webhook to extract chapters for '{book_title}'...")
    
    max_retries = 3
    retry_delay = 5
    
    for attempt in range(max_retries):
        try:
            async with session.post(WEBHOOK_URL_1, json=payload_1) as response_1:
                response_1.raise_for_status()
                chapters_response = await response_1.json()
                
                if isinstance(chapters_response, dict) and "chapters" in chapters_response:
                    chapters = chapters_response["chapters"]
                elif isinstance(chapters_response, list):
                    chapters = chapters_response
                else:
                    print("Expected the first webhook to return a list of chapters (or an object with a 'chapters' array).")
                    return None

                print(f"First webhook successful. Received {len(chapters)} chapters.\n")
                return chapters
        except aiohttp.ClientError as e:
            if attempt < max_retries - 1:
                print(f"Attempt {attempt + 1} failed for first webhook: {e}. Retrying in {retry_delay} seconds...")
                await asyncio.sleep(retry_delay)
            else:
                print(f"Error making first webhook call after {max_retries} attempts: {e}")
                return None
        except ValueError:
            print("First webhook response is not valid JSON.")
            return None

async def process_chapter(session, chapter_number, chapter_title, chapter_content, book_title, final_modes, output_dirs):
    try:
        ch_num_padded = f"{int(chapter_number):02d}"
    except (ValueError, TypeError):
        ch_num_padded = str(chapter_number).zfill(2)
    
    filename = f"{ch_num_padded}-{slugify(chapter_title)}.md"
    
    # Check if files already exist in all output directories
    all_exist = True
    for output_dir in output_dirs:
        filepath = os.path.join(output_dir, filename)
        if not os.path.exists(filepath):
            all_exist = False
            break
            
    if all_exist:
        print(f"Skipping Chapter {chapter_number}: {chapter_title} (already exists)")
        return

    payload_2 = {
        "mode": final_modes[0],
        "metadata": {
            "title": book_title
        },
        "content": {
            "bodyMatter": {
                "chapterNumber": chapter_number,
                "title": chapter_title,
                "content": chapter_content
            }
        }
    }

    print(f"Sending second webhook for Chapter {chapter_number}: {chapter_title}...")
    
    max_retries = 3
    retry_delay = 5
    
    for attempt in range(max_retries):
        try:
            async with session.post(WEBHOOK_URL_2, json=payload_2) as response_2:
                response_2.raise_for_status()
                
                try:
                    rule_response = await response_2.json()
                    if isinstance(rule_response, dict) and "rule" in rule_response:
                        webhook_2_result = rule_response["rule"]
                    else:
                        webhook_2_result = await response_2.text()
                except Exception:
                    webhook_2_result = await response_2.text()

            for output_dir in output_dirs:
                filepath = os.path.join(output_dir, filename)
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(webhook_2_result)
                print(f"  -> Saved response to {filepath}")
            return

        except aiohttp.ClientError as e:
            if attempt < max_retries - 1:
                print(f"Attempt {attempt + 1} failed for chapter {chapter_number}: {e}. Retrying in {retry_delay} seconds...")
                await asyncio.sleep(retry_delay)
            else:
                print(f"Error making second webhook call for chapter {chapter_number} after {max_retries} attempts: {e}")

async def process_chapters_for_modes(session, final_modes, book_title, chapters, content):
    sanitized_book_title = slugify(book_title)
    
    output_dirs = []
    for mode_name in final_modes:
        output_dir = os.path.join("rules", mode_name, sanitized_book_title)
        os.makedirs(output_dir, exist_ok=True)
        output_dirs.append(output_dir)

    print(f"\n--- Processing {len(chapters)} chapters concurrently for modes: {', '.join(final_modes)} ---")

    tasks = []
    for i, chapter in enumerate(chapters):
        if isinstance(chapter, dict):
            chapter_number = chapter.get("chapterNumber", i + 1)
            chapter_title = chapter.get("title", f"Chapter {chapter_number}")
            chapter_content = chapter.get("content", content)
        elif isinstance(chapter, str):
            chapter_number = i + 1
            chapter_title = chapter
            chapter_content = content
            
            match = re.match(r"^Chapter\s+(\d+)[:\-\s]+(.*)", chapter, re.IGNORECASE)
            if match:
                chapter_number = int(match.group(1))
                chapter_title = match.group(2).strip()
        else:
            print(f"Unexpected chapter format: {type(chapter)}")
            continue

        tasks.append(process_chapter(
            session, chapter_number, chapter_title, chapter_content, 
            book_title, final_modes, output_dirs
        ))

    # Run all chapter webhooks concurrently
    await asyncio.gather(*tasks)

async def async_main():
    parser = argparse.ArgumentParser(description="Process a book file and generate rules for multiple modes.")
    parser.add_argument("args", nargs='+', help="Mode names (comma or space separated) followed by the book file path as the last argument.")

    parsed_args = parser.parse_args()
    
    if len(parsed_args.args) < 2:
        print("Error: Must provide at least one mode and the book file path.")
        sys.exit(1)

    book_file_path = parsed_args.args[-1]
    modes_string = " ".join(parsed_args.args[:-1])
    
    final_modes = [m.strip() for m in re.split(r'[\s,]+', modes_string) if m.strip()]

    if not os.path.exists(book_file_path):
        print(f"Error: File not found at {book_file_path}")
        sys.exit(1)

    try:
        with open(book_file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    book_title = os.path.splitext(os.path.basename(book_file_path))[0]

    async with aiohttp.ClientSession() as session:
        chapters = await get_chapters(session, book_title, content)
        if not chapters:
            print("Could not retrieve chapters. Exiting.")
            sys.exit(1)

        if final_modes:
            await process_chapters_for_modes(session, final_modes, book_title, chapters, content)

def main():
    try:
        asyncio.run(async_main())
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
