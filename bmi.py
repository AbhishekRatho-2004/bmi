import streamlit as st
import random

# Define the knowledge base
knowledge_base = {
    "protein": {
        "chicken breast": 31,
        "salmon": 22,
        "tofu": 8,
        "lentils": 9,
        "black beans": 7,
    },
    "carbohydrates": {
        "brown rice": 45,
        "quinoa": 39,
        "sweet potato": 27,
        "whole wheat bread": 18,
        "oats": 17,
    },
    "fats": {
        "avocado": 15,
        "almonds": 14,
        "peanut butter": 8,
        "olive oil": 0,
        "chia seeds": 5,
    },
    "vitamins and minerals": {
        "spinach": 145,
        "kale": 200,
        "broccoli": 81,
        "bell pepper": 95,
        "carrot": 41,
    },
}

def suggest_diet(weight, height, age, gender):
    # Calculate the basal metabolic rate
    if gender.lower() == "male":
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)

    # Calculate the daily caloric needs
    daily_caloric_needs = bmr * 1.2  # Assuming sedentary lifestyle

    # Calculate the nutrient recommendations
    recommendations = {}
    for nutrient in knowledge_base.keys():
        nutrient_recommendation = 0
        for food in knowledge_base[nutrient]:
            nutrient_recommendation += knowledge_base[nutrient][food] * knowledge_base.get(nutrient).get(food)
        recommendations[nutrient] = nutrient_recommendation * daily_caloric_needs / 2000  # Convert to daily values based on 2000 calorie diet

    return recommendations

def suggest_meal_plan(diet_type, num_courses):
    meal_plan = []

    # Determine the nutrient recommendations based on diet type
    if diet_type.lower() == "vegan":
        nutrient_preferences = ["carbohydrates", "vitamins and minerals"]
    elif diet_type.lower() == "vegetarian":
        nutrient_preferences = ["protein", "carbohydrates", "vitamins and minerals"]
    elif diet_type.lower() == "non-vegetarian":
        nutrient_preferences = ["protein", "carbohydrates", "fats", "vitamins and minerals"]
    else:
        st.error("Invalid diet type entered. Please try again.")
        return []

    # Generate the meal plan
    for course_num in range(num_courses):
        course = {}
        for nutrient in nutrient_preferences:
            food_options = knowledge_base[nutrient]
            random_food = random.choice(list(food_options.keys()))
            course[nutrient] = random_food
        meal_plan.append(course)

    return meal_plan

# Streamlit UI
st.title("Nutrient Suggestion and Meal Planning App")

# Get user information
weight = st.number_input("What is your weight in kilograms?", min_value=1)
height = st.number_input("What is your height in centimeters?", min_value=1)
age = st.number_input("What is your age in years?", min_value=1)
gender = st.radio("What is your gender?", ["Male", "Female"])

# BMI Calculation and Display
bmi = weight / ((height / 100) ** 2)
st.write(f"Your BMI is: {bmi:.2f}")

if 18.5 <= bmi < 24.9:
    st.write('Healthy weight')
elif 24.9 <= bmi < 29.9:
    st.write('Overweight')
else:
    st.write('Obese')

# Suggest daily nutrient recommendations based on user information
recommendations = suggest_diet(weight, height, age, gender)
st.write("\nBased on your information, the following daily nutrient recommendations are suggested:")
for nutrient, recommendation in recommendations.items():
    st.write(f"{nutrient.capitalize()}: {recommendation:.2f} g")

# Get user input for meal plan generation
diet_type = st.selectbox("What type of diet would you like?", ["Vegan", "Vegetarian", "Non-vegetarian"])
num_courses = st.number_input("How many courses would you like in your meal plan?", min_value=1)

# Generate and display the meal plan
meal_plan = suggest_meal_plan(diet_type, num_courses)
st.write("\nHere is your suggested meal plan:")
for course_num, course in enumerate(meal_plan):
    st.write(f"\nCourse {course_num + 1}:")
    for nutrient, food in course.items():
        st.write(f"{nutrient.capitalize()}: {food}")