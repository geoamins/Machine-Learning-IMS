import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

def scrape_movie_data():
    """
    Scrapes movie data from IMDB's Top 250 movies list
    """
    # URL of IMDB's Top 250 movies (using legacy version)
    url = "https://www.imdb.com/chart/top/?ref_=nv_mv_250"
    
    # Add more comprehensive headers to mimic a browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0',
        'Cookie': 'lc-main=en_US'  # Request English version
    }
    
    try:
        # Send GET request
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        print(f"Response status: {response.status_code}")
        print(f"Content length: {len(response.text)}")
        
        # Parse HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Try to find the movie list container
        movies = soup.select('tbody.lister-list tr')
        if not movies:
            movies = soup.select('.ipc-metadata-list-summary-item')
        
        print(f"Found {len(movies)} movies in the HTML")
        
        if len(movies) == 0:
            print("No movies found. Printing first 500 characters of HTML for debugging:")
            print(response.text[:500])
            return
        
        # Initialize lists to store data
        titles = []
        years = []
        ratings = []
        
        # Extract data for each movie
        for movie in movies:
            try:
                # Try different selectors for title
                title_elem = (
                    movie.select_one('td.titleColumn a') or 
                    movie.select_one('.ipc-title__text') or
                    movie.select_one('.ipc-metadata-list-summary-item__t')
                )
                
                if title_elem:
                    title = title_elem.text.strip()
                    if title.startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.')):
                        title = title.split(' ', 1)[1]
                    titles.append(title)
                else:
                    print("Could not find title element")
                    continue
                
                # Try different selectors for year
                year_elem = (
                    movie.select_one('span.secondaryInfo') or
                    movie.select_one('.cli-title-metadata span') or
                    movie.select_one('.ipc-metadata-list-summary-item__metadata')
                )
                
                if year_elem:
                    year = year_elem.text.strip('()')
                    years.append(year)
                else:
                    print("Could not find year element")
                    continue
                
                # Try different selectors for rating
                rating_elem = (
                    movie.select_one('td.ratingColumn strong') or
                    movie.select_one('.ipc-rating-star--imdb') or
                    movie.select_one('.cli-ratings-container span')
                )
                
                if rating_elem:
                    rating = rating_elem.text.strip()
                    ratings.append(rating)
                else:
                    print("Could not find rating element")
                    continue
                
                print(f"Successfully scraped: {title} ({year}) - {rating}")
                
                # Add a small delay to be polite
                time.sleep(random.uniform(0.5, 1.5))
                
            except Exception as e:
                print(f"Error processing a movie: {e}")
                continue
        
        print(f"\nTotal movies scraped: {len(titles)}")
        
        if len(titles) > 0:
            # Create DataFrame
            df = pd.DataFrame({
                'Title': titles,
                'Year': years,
                'Rating': ratings
            })
            
            # Save to CSV
            output_path = 'Web Scraping Presentation/top_movies.csv'
            df.to_csv(output_path, index=False, encoding='utf-8')
            print(f"\nData successfully scraped and saved to '{output_path}'")
            print(f"First few entries:")
            print(df.head())
        else:
            print("\nNo movies were scraped successfully.")
        
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    scrape_movie_data() 