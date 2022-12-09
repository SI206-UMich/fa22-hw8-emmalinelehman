import matplotlib.pyplot as plt
import os
import sqlite3
import unittest


def get_restaurant_data(db_filename):
    """
    This function accepts the file name of a database as a parameter and returns a list of
    dictionaries. Each dictionary will contain the information for one restaurant. 
    The key:value pairs should be the name, category_id, building_id, and rating
    of each restaurant in the database.
    """
    conn = sqlite3.connect(db_filename)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Restaurants")
    list_of_restaurants = []
    for row in cur.fetchall():
        row_dict = {}
        row_dict['name'] = row[1]
        row_dict['category'] = row[2]
        row_dict['building'] = row[3]
        row_dict['rating'] = row[4]
        list_of_restaurants.append(row_dict)
    conn.close()
    return list_of_restaurants



def barchart_restaurant_categories(db_filename):
    '''
    The barchart_restaurant_categories(db_filename) function that accepts the filename of the database as a parameter, and returns a dictionary.
    The dictionary should have the category_id as the key and the number of restaurants in that category as the value.
    This function should also create a bar graph that displays the names of the categories along the y-axis and the number of restaurants in each category along the x-axis.
    '''
    conn = sqlite3.connect(db_filename)
    conn = sqlite3.connect(db_filename)
    cur = conn.cursor()
    cur.execute("SELECT category_id, COUNT(category_id) FROM Restaurants GROUP BY category_id")
    category_data = {}
    for row in cur:
        category_data[row[0]] = row[1]
    conn.close()
    #print(category_data)
    plt.barh(list(category_data.keys()), list(category_data.values()))
    plt.xlabel("Number of Restaurants")
    plt.ylabel("Category")
    plt.show()
    return category_data



#EXTRA CREDIT
def highest_rated_category(db_filename):#Do this through DB as well
    """
    This function finds the average restaurant rating for each category and returns a tuple containing the
    category name of the highest rated restaurants and the average rating of the restaurants
    in that category. This function should also create a bar graph that displays the categories along the y-axis
    and their ratings along the x-axis in descending order (by rating).
    """
    conn = sqlite3.connect(db_filename)
    cur = conn.cursor()
    cur.execute("SELECT category_id, AVG(rating) FROM Restaurants GROUP BY category_id")
    category_data = {}
    for row in cur:
        category_data[row[0]] = row[1]
    conn.close()
    #print(category_data)
    plt.barh(list(category_data.keys()), list(category_data.values()))
    plt.xlabel("Average Rating")
    plt.ylabel("Category")
    plt.show()
    return max(category_data, key=category_data.get), category_data[max(category_data, key=category_data.get)]



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
