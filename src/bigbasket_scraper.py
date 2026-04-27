from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

url = "https://www.bigbasket.com/ps/?q=rice"

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install())
)

driver.get(url)
time.sleep(5)

# -----------------------------
# STEP 1: Auto Scroll
# -----------------------------
last_height = driver.execute_script(
    "return document.body.scrollHeight"
)

for _ in range(8):
    driver.execute_script(
        "window.scrollTo(0, document.body.scrollHeight);"
    )
    time.sleep(3)

    new_height = driver.execute_script(
        "return document.body.scrollHeight"
    )

    if new_height == last_height:
        break

    last_height = new_height

# -----------------------------
# STEP 2: Extract Data
# -----------------------------
products = []
prices = []
ratings = []

cards = driver.find_elements(By.TAG_NAME, "h3")

for card in cards[:100]:
    try:
        product_name = card.text.strip()

        if product_name:
            products.append(product_name)

    except:
        products.append(None)

# Price extraction (example selector)
price_elements = driver.find_elements(
    By.XPATH,
    "//span[contains(text(),'₹')]"
)

for p in price_elements[:100]:
    try:
        prices.append(p.text.strip())
    except:
        prices.append(None)

# Rating extraction (optional)
rating_elements = driver.find_elements(
    By.XPATH,
    "//span[contains(@class,'Label-sc')]"
)

for r in rating_elements[:100]:
    try:
        ratings.append(r.text.strip())
    except:
        ratings.append(None)

driver.quit()

# -----------------------------
# STEP 3: Equal Length Fix
# -----------------------------
max_len = max(len(products), len(prices), len(ratings))

products += [None] * (max_len - len(products))
prices += [None] * (max_len - len(prices))
ratings += [None] * (max_len - len(ratings))

# -----------------------------
# STEP 4: Save CSV
# -----------------------------
df = pd.DataFrame({
    "Product_Name": products,
    "Current_Price": prices,
    "Rating": ratings
})

df["Timestamp"] = pd.Timestamp.now()

df.to_csv(
    "data/external/competitor_prices.csv",
    index=False
)

print(df.head(20))
print(f"Total rows scraped: {len(df)}")