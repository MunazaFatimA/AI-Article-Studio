import os
import requests
import time


try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

def fetch_images(keyword, per_page=4, max_retries=3):
    """
    Fetch images from Unsplash, fallback to Pexels
    Enhanced with better error handling and logging
    """
    
    if not keyword:
        print("❌ No keyword provided")
        return []
    
    print(f"🔍 Fetching images for keyword: {keyword}")
    
    # ============================================================
    # TRY UNSPLASH FIRST
    # ============================================================
    for attempt in range(max_retries):
        try:
            api_key = os.getenv("UNSPLASH_API_KEY")
            if not api_key or len(api_key) < 5:
                print("⚠️ Unsplash API key not configured")
                break
            
            # Clean keyword for URL
            clean_keyword = keyword.replace(" ", "%20")[:100]
            url = f"https://api.unsplash.com/search/photos?query={clean_keyword}&per_page={per_page}&orientation=landscape"
            headers = {"Authorization": f"Client-ID {api_key}"}
            
            print(f"  📡 Attempt {attempt + 1}: Calling Unsplash API...")
            response = requests.get(url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                results = data.get("results", [])
                if results:
                    images = []
                    for img in results[:per_page]:
                        img_url = img.get("urls", {}).get("regular")
                        if img_url:
                            images.append(img_url)
                    
                    if images:
                        print(f"  ✅ Unsplash: Successfully fetched {len(images)} images")
                        return images
                else:
                    print(f"  ⚠️ Unsplash: No results for '{keyword}'")
                    
            elif response.status_code == 401:
                print("  ❌ Unsplash: Invalid API key (401)")
                break  # Don't retry, it's an auth error
                
            elif response.status_code == 403:
                print("  ❌ Unsplash: Access forbidden (403)")
                break
                
            elif response.status_code == 429:
                print(f"  ⚠️ Unsplash: Rate limited (429). Waiting {2**attempt}s...")
                time.sleep(2 ** attempt)  # Exponential backoff
                continue
                
            else:
                print(f"  ⚠️ Unsplash: HTTP {response.status_code}")
                if attempt < max_retries - 1:
                    time.sleep(1)
                    
        except requests.exceptions.Timeout:
            print(f"  ⚠️ Unsplash: Connection timeout (attempt {attempt + 1})")
            if attempt < max_retries - 1:
                time.sleep(1)
                
        except Exception as e:
            print(f"  ⚠️ Unsplash error: {str(e)[:80]}")
            if attempt < max_retries - 1:
                time.sleep(1)
    
    print("  → Unsplash failed, trying Pexels...")
    
    # ============================================================
    # TRY PEXELS AS BACKUP
    # ============================================================
    for attempt in range(max_retries):
        try:
            pexels_key = os.getenv("PEXELS_API_KEY")
            if not pexels_key or len(pexels_key) < 5:
                print("⚠️ Pexels API key not configured")
                break
            
            # Clean keyword for URL
            clean_keyword = keyword.replace(" ", "%20")[:100]
            url = f"https://api.pexels.com/v1/search?query={clean_keyword}&per_page={per_page}&orientation=landscape"
            headers = {"Authorization": pexels_key}
            
            print(f"  📡 Attempt {attempt + 1}: Calling Pexels API...")
            response = requests.get(url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                photos = data.get("photos", [])
                if photos:
                    images = []
                    for img in photos[:per_page]:
                        # Pexels provides multiple URLs, prefer 'large'
                        img_url = img.get("src", {}).get("large") or img.get("src", {}).get("medium")
                        if img_url:
                            images.append(img_url)
                    
                    if images:
                        print(f"  ✅ Pexels: Successfully fetched {len(images)} images")
                        return images
                else:
                    print(f"  ⚠️ Pexels: No results for '{keyword}'")
                    
            elif response.status_code == 401:
                print("  ❌ Pexels: Invalid API key (401)")
                break
                
            elif response.status_code == 403:
                print("  ❌ Pexels: Access forbidden (403)")
                break
                
            elif response.status_code == 429:
                print(f"  ⚠️ Pexels: Rate limited (429). Waiting {2**attempt}s...")
                time.sleep(2 ** attempt)
                continue
                
            else:
                print(f"  ⚠️ Pexels: HTTP {response.status_code}")
                if attempt < max_retries - 1:
                    time.sleep(1)
                    
        except requests.exceptions.Timeout:
            print(f"  ⚠️ Pexels: Connection timeout (attempt {attempt + 1})")
            if attempt < max_retries - 1:
                time.sleep(1)
                
        except Exception as e:
            print(f"  ⚠️ Pexels error: {str(e)[:80]}")
            if attempt < max_retries - 1:
                time.sleep(1)
    
    print("  ❌ Both image sources failed")
    return []


def get_fallback_images():
    """
    Get a list of free stock image URLs that don't require API calls
    Useful as ultimate fallback
    """
    # These are stable free image URLs that can be used as fallback
    fallback_urls = [
        "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=800&q=80",  # AI/Tech
        "https://images.unsplash.com/photo-1461896836934-ffe607ba8211?w=800&q=80",  # Tech/Data
        "https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=800&q=80",  # Business
        "https://images.unsplash.com/photo-1552664730-d307ca884978?w=800&q=80",   # Growth
        "https://images.unsplash.com/photo-1552664730-d307ca884978?w=800&q=80",   # Success
    ]
    return fallback_urls[:4]