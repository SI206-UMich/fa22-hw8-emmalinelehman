import matplotlib.pyplot as plt
import os
import sqlite3
import unittest


def get_restaurant_data(db_filename):
    """
    This function accepts the file name of a database as a parameter and returns a list of
    dictionaries. Each dictionary will contain the information for one restaurant. 
    The keys should be the name, category, building, and rating of each restaurant in the database. The values should be the text and information for each restaurant.
    """
    #Expected return value:[{‘name’: ‘M-36 Coffee Roasters Cafe’, ‘category’: ‘Cafe’, ‘building’: 1101, ‘rating’: 3.8}, . . . ]

    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_filename)
    cur = conn.cursor()
    cur.execute(
        """
        SELECT name, category, building, rating 
        FROM restaurants
        JOIN categories
        ON restaurants.category_id = categories.id
        JOIN buildings
        ON restaurants.building_id = buildings.id
        """
    )
    data = cur.fetchall()
    restaurant_information = []
    for i in data:
        whole_stats = {}
        whole_stats['name'] = i[0]
        whole_stats['category'] = i[1]
        whole_stats['building'] = i[2]
        whole_stats['rating'] = i[3]
        restaurant_information.append(whole_stats)
    return restaurant_information




def barchart_restaurant_categories(db_filename):
    '''
    The barchart_restaurant_categories(db_filename) function that accepts the filename of the database as a parameter, and returns a dictionary.
    The dictionary should have the category_id as the key and the number of restaurants in that category as the value.
    This function should also create a bar graph that displays the names of the categories along the y-axis and the number of restaurants in each category along the x-axis.
    '''
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_filename)
    cur = conn.cursor()
    cur.execute(
        """
        SELECT category, COUNT(category_id) 
        FROM restaurants 
        JOIN categories 
        ON restaurants.category_id = categories.id 
        GROUP BY category_id
        ORDER BY COUNT(category_id) ASC
        """
    )
    data = cur.fetchall()
    category_dict = {}
    for i in data:
        category_dict[i[0]] = category_dict.get(i, 0) + i[1]

    categories = list(category_dict.keys())
    val_list = list(category_dict.values())
    plt.barh(categories, val_list)
    plt.ylabel("Restaurant Categories")
    plt.xlabel("Number of Restaurants")
    plt.title("Types of Restaurants in S. University")
    plt.tight_layout()
    plt.show()
    return category_dict




#EXTRA CREDIT
def highest_rated_category(db_filename):#Do this through DB as well
    """
    This function finds the average restaurant rating for each category and returns a tuple containing the
    category name of the highest rated restaurants and the average rating of the restaurants
    in that category. This function should also create a bar graph that displays the categories along the y-axis
    and their ratings along the x-axis in descending order (by rating).
    """
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_filename)
    cur = conn.cursor()
    cur.execute(
        """
        SELECT category, rating
        FROM restaurants 
        JOIN categories 
        ON restaurants.category_id = categories.id 
        GROUP BY category_id
        ORDER BY rating ASC
        """
    )
    data = cur.fetchall()
    highest_dict = {}
    for z in data:
        highest_dict[z[0]] = highest_dict.get(z, 0) + z[1]
    categories = list(highest_dict.keys())
    high_vals = list(highest_dict.values())
    plt.barh(categories, high_vals)
    plt.ylabel("Categories")
    plt.xlabel("Ratings")
    plt.title("Average Restaurant Ratings by Category")
    plt.tight_layout()
    plt.show()
    return data[-1]


#Try calling your functions here
def main():
    get_restaurant_data('South_U_Restaurants.db')
    barchart_restaurant_categories('South_U_Restaurants.db')
    highest_rated_category('South_U_Restaurants.db')

class TestHW8(unittest.TestCase):
    def setUp(self):
        self.rest_dict = {
            'name': 'M-36 Coffee Roasters Cafe',
            'category': 'Cafe',
            'building': 1101,
            'rating': 3.8
        }
        self.cat_dict = {
            'Asian Cuisine ': 2,
            'Bar': 4,
            'Bubble Tea Shop': 2,
            'Cafe': 3,
            'Cookie Shop': 1,
            'Deli': 1,
            'Japanese Restaurant': 1,
            'Juice Shop': 1,
            'Korean Restaurant': 2,
            'Mediterranean Restaurant': 1,
            'Mexican Restaurant': 2,
            'Pizzeria': 2,
            'Sandwich Shop': 2,
            'Thai Restaurant': 1
        }
        self.best_category = ('Deli', 4.6)

    def test_get_restaurant_data(self):
        rest_data = get_restaurant_data('South_U_Restaurants.db')
        self.assertIsInstance(rest_data, list)
        self.assertEqual(rest_data[0], self.rest_dict)
        self.assertEqual(len(rest_data), 25)

    def test_barchart_restaurant_categories(self):
        cat_data = barchart_restaurant_categories('South_U_Restaurants.db')
        self.assertIsInstance(cat_data, dict)
        self.assertEqual(cat_data, self.cat_dict)
        self.assertEqual(len(cat_data), 14)

    def test_highest_rated_category(self):
        best_category = highest_rated_category('South_U_Restaurants.db')
        self.assertIsInstance(best_category, tuple)
        self.assertEqual(best_category, self.best_category)

if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)
