"""
Update the hotel recommendation model with comprehensive hotel data
"""
import pickle
import pandas as pd
import numpy as np

print("🔄 Updating Hotel Recommendation Model with comprehensive data...")
print("=" * 60)

# Define the CFRecommender class
class CFRecommender:
    MODEL_NAME = 'Collaborative Filtering'

    def __init__(self, cf_predictions_df, items_df):
        self.cf_predictions_df = cf_predictions_df
        self.items_df = items_df

    def get_model_name(self):
        return self.MODEL_NAME

    def recommend_items(self, place, days, budget, topn=5):
        # Filter available hotels based on place, days, and budget
        filtered_hotels = self.items_df[
            (self.items_df["place"] == place) &
            (self.items_df["days"] == days) &
            (self.items_df["price"] <= budget)
        ]

        if filtered_hotels.empty:
            return pd.DataFrame()  # No hotels match criteria

        # Get top recommended hotels sorted by price
        recommendations_df = filtered_hotels.groupby("name")["price"].min().reset_index()
        recommendations_df = recommendations_df.sort_values(by="price", ascending=True).head(topn)

        return recommendations_df

# Create comprehensive hotel data
print("\n📊 Creating comprehensive hotel database...")

cities = ['Paris', 'Barcelona', 'London', 'Rome', 'Amsterdam', 'Berlin', 'Madrid', 'Vienna']
hotel_names = {
    'Paris': ['Eiffel Tower Hotel', 'Louvre Palace', 'Champs Elysees Inn', 'Seine Riverside', 'Montmartre View', 
              'Arc de Triomphe Suites', 'Notre Dame Lodge', 'Versailles Grand', 'Latin Quarter Hotel', 'Marais Boutique'],
    'Barcelona': ['Sagrada Familia Hotel', 'Beachfront Resort', 'Gothic Quarter Inn', 'Ramblas Central', 'Park Guell View',
                  'Barceloneta Beach', 'Las Ramblas Hotel', 'Montjuic Palace', 'Eixample Suites', 'Gracia Boutique'],
    'London': ['Big Ben Hotel', 'Thames Riverside', 'Hyde Park Inn', 'Westminster Suites', 'Covent Garden Lodge',
               'Tower Bridge View', 'Piccadilly Central', 'Camden Market Hotel', 'Shoreditch Boutique', 'Kensington Palace'],
    'Rome': ['Colosseum Hotel', 'Vatican View', 'Trevi Fountain Inn', 'Spanish Steps Suites', 'Pantheon Lodge',
             'Trastevere Boutique', 'Roman Forum Hotel', 'Villa Borghese Inn', 'Campo de Fiori', 'Testaccio Central'],
    'Amsterdam': ['Canal View Hotel', 'Anne Frank House Inn', 'Rijksmuseum Suites', 'Jordaan Boutique', 'Red Light District Lodge',
                  'Vondelpark Hotel', 'Dam Square Central', 'Leidseplein Inn', 'Museum Quarter', 'De Pijp Suites'],
    'Berlin': ['Brandenburg Gate Hotel', 'Checkpoint Charlie Inn', 'Museum Island Suites', 'Potsdamer Platz', 'Kreuzberg Boutique',
               'Alexanderplatz Hotel', 'Charlottenburg Palace', 'Friedrichshain Lodge', 'Mitte Central', 'Prenzlauer Berg Inn'],
    'Madrid': ['Prado Museum Hotel', 'Retiro Park Inn', 'Gran Via Suites', 'Plaza Mayor Lodge', 'Salamanca Boutique',
               'Royal Palace View', 'Malasana Hotel', 'Chueca Central', 'La Latina Inn', 'Huertas Suites'],
    'Vienna': ['Schonbrunn Palace Hotel', 'St. Stephens Cathedral Inn', 'Ringstrasse Suites', 'Belvedere View', 'Naschmarkt Lodge',
               'Museumsquartier Hotel', 'Prater Park Inn', 'Hofburg Central', 'Graben Boutique', 'Leopoldstadt Suites']
}

# Generate comprehensive hotel data
hotels_data = []
np.random.seed(42)

for city in cities:
    city_hotels = hotel_names.get(city, [f'{city} Hotel {i}' for i in range(1, 11)])
    
    for hotel_name in city_hotels:
        # Create multiple entries for different day ranges and price points
        for days in range(1, 31):  # 1 to 30 days
            # Base price varies by hotel type
            base_price = np.random.uniform(50, 300)
            
            # Price variations for different day ranges
            if days <= 3:
                price = base_price * (1 + np.random.uniform(-0.2, 0.3))  # Short stays
            elif days <= 7:
                price = base_price * (1 + np.random.uniform(-0.1, 0.2))  # Medium stays
            else:
                price = base_price * (1 + np.random.uniform(-0.3, 0.1))  # Long stays (discount)
            
            # Ensure price is reasonable
            price = max(30, min(500, price))
            
            hotels_data.append({
                'name': hotel_name,
                'place': city,
                'days': days,
                'price': round(price, 2)
            })

items_df = pd.DataFrame(hotels_data)
cf_predictions_df = pd.DataFrame()  # Empty for this model type

# Create model instance
model = CFRecommender(cf_predictions_df, items_df)

# Save updated model
print(f"\n💾 Saving updated model...")
print(f"   Total hotels: {len(items_df)}")
print(f"   Cities: {sorted(items_df['place'].unique())}")
print(f"   Days range: {items_df['days'].min()} - {items_df['days'].max()}")
print(f"   Price range: ${items_df['price'].min():.2f} - ${items_df['price'].max():.2f}")

with open('cf_recommender.pkl', 'wb') as f:
    pickle.dump(model, f)

print("   ✓ Saved: cf_recommender.pkl")

# Test recommendations
print("\n🧪 Testing recommendations...")
test_cases = [
    ('Paris', 3, 200),
    ('Barcelona', 5, 150),
    ('London', 7, 250),
    ('Rome', 2, 100),
    ('Amsterdam', 4, 180)
]

for city, days, budget in test_cases:
    recs = model.recommend_items(city, days, budget, topn=3)
    if not recs.empty:
        print(f"   ✓ {city}, {days} days, ${budget} budget: {len(recs)} hotels found")
    else:
        print(f"   ⚠️  {city}, {days} days, ${budget} budget: No hotels found")

print("\n✅ Hotel data updated successfully!")
print("=" * 60)
print("\n🔄 Please restart the Streamlit app to see the changes:")
print("   1. Stop current app: pkill -f streamlit")
print("   2. Restart: cd 'Travel Recommendation Model' && streamlit run app.py")

