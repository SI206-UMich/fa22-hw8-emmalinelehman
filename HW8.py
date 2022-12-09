import matplotlib.pyplot as plt
import os
import sqlite3
import unittest


def get_restaurant_data(db_filename):
    '''
    complete the get_restaurant_data(db_filename) function that accepts the filename of the database as a parameter, and returns a list of dictionaries.
    In each dictionary, the key:value pairs should be the name of the restaurant, the category_id , building_id, and rating for each restaurant.
    '''
    list_of_restaurants = []
    conn = sqlite3.connect(db_filename)
    cur = conn.cursor()
    cur.execute('SELECT name, category_id, building_id, rating FROM Restaurants')
    for row in cur:
        list_of_restaurants.append({'name': row[0], 'category': row[1], 'building': row[2], 'rating': row[3]})
    conn.close()
    return list_of_restaurants


def barchart_restaurant_categories(db_filename):
    """
    This function accepts a file name of a database as a parameter and returns a dictionary. The keys should be the
    restaurant categories and the values should be the number of restaurants in each category. The function should
    also create a bar chart with restaurant categories and the counts of each category.
    """
    conn = sqlite3.connect(db_filename)
    cur = conn.cursor()
    cur.execute('SELECT category_id, COUNT(category_id) FROM Restaurants GROUP BY category_id')
    category_dict = {}
    for row in cur:
        category_dict[row[0]] = row[1]
    conn.close()
    plt.bar(range(len(category_dict)), list(category_dict.values()), align='center')
    plt.xticks(range(len(category_dict)), list(category_dict.keys()))
    plt.show()
    return category_dict


#EXTRA CREDIT
def highest_rated_category(db_filename):#Do this through DB as well
    """
    This function finds the average restaurant rating for each category and returns a tuple containing the
    category name of the highest rated restaurants and the average rating of the restaurants
    in that category. This function should also create a bar chart that displays the categories along the y-axis
    and their ratings along the x-axis in descending order (by rating).
    """
    conn = sqlite3.connect(db_filename)
    cur = conn.cursor()
    cur.execute('SELECT category_id, AVG(rating) FROM Restaurants GROUP BY category_id')
    category_dict = {}
    for row in cur:
        category_dict[row[0]] = row[1]
    conn.close()
    plt.barh(range(len(category_dict)), list(category_dict.values()), align='center')
    plt.yticks(range(len(category_dict)), list(category_dict.keys()))
    plt.show()
    return max(category_dict.items(), key=lambda x: x[1])

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
