"""
Create Comprehensive Real-World Datasets for SmartML Demo
All datasets have meaningful patterns and realistic relationships
"""
import pandas as pd
import numpy as np

# Set random seed for reproducibility
np.random.seed(42)

# ==========================================
# 1. E-COMMERCE CUSTOMER DATA
# ==========================================
print("Creating E-Commerce Customer Dataset...")

n_customers = 500

# Customer Demographics (realistic distributions)
ages = np.random.normal(35, 12, n_customers).clip(18, 70).astype(int)
account_age_months = np.random.exponential(24, n_customers).clip(1, 60).astype(int)

# Income based on age (realistic relationship)
income = 25000 + ages * 800 + np.random.normal(0, 10000, n_customers)
income = income.clip(20000, 150000).round(0)

# Shopping behavior (correlated with income and age)
monthly_purchases = (income / 10000 + np.random.normal(5, 2, n_customers)).clip(1, 20).astype(int)
avg_order_value = (income / 500 + np.random.normal(50, 20, n_customers)).clip(20, 500).round(2)

# Total spending (meaningful relationship)
total_spent = monthly_purchases * avg_order_value * account_age_months
total_spent = total_spent + np.random.normal(0, 500, n_customers)
total_spent = total_spent.clip(100, 50000).round(2)

# Time on site (minutes per session)
time_on_site = (monthly_purchases * 3 + np.random.normal(10, 5, n_customers)).clip(2, 60).round(1)

# Product views (correlated with purchases)
product_views = (monthly_purchases * 8 + np.random.normal(20, 10, n_customers)).clip(5, 200).astype(int)

# Cart abandonment rate (inversely related to purchases)
cart_abandonment_rate = (0.8 - monthly_purchases * 0.02 + np.random.normal(0, 0.1, n_customers)).clip(0.1, 0.9).round(2)

# Customer satisfaction (1-5, influenced by spending behavior)
satisfaction_score = (3 + monthly_purchases * 0.1 + np.random.normal(0, 0.5, n_customers)).clip(1, 5).round(1)

# Loyalty status (based on total spent and account age) - CLASSIFICATION TARGET
loyalty_tier = []
for i in range(n_customers):
    if total_spent[i] > 15000 and account_age_months[i] > 12:
        loyalty_tier.append('Premium')
    elif total_spent[i] > 5000 or account_age_months[i] > 6:
        loyalty_tier.append('Gold')
    else:
        loyalty_tier.append('Silver')

# Churn prediction (binary classification) - realistic pattern
churn = []
for i in range(n_customers):
    churn_prob = 0.3  # base churn rate
    if monthly_purchases[i] < 3:
        churn_prob += 0.3
    if satisfaction_score[i] < 3:
        churn_prob += 0.2
    if cart_abandonment_rate[i] > 0.6:
        churn_prob += 0.15
    churn.append(1 if np.random.random() < churn_prob else 0)

# Region (categorical)
regions = np.random.choice(['North', 'South', 'East', 'West', 'Central'], n_customers, 
                          p=[0.25, 0.20, 0.25, 0.20, 0.10])

# Device type
devices = np.random.choice(['Mobile', 'Desktop', 'Tablet'], n_customers, 
                          p=[0.55, 0.35, 0.10])

ecommerce_df = pd.DataFrame({
    'CustomerID': range(1, n_customers + 1),
    'Age': ages,
    'AnnualIncome': income,
    'AccountAgeMonths': account_age_months,
    'MonthlyPurchases': monthly_purchases,
    'AvgOrderValue': avg_order_value,
    'TotalSpent': total_spent,
    'TimeOnSiteMinutes': time_on_site,
    'ProductViews': product_views,
    'CartAbandonmentRate': cart_abandonment_rate,
    'SatisfactionScore': satisfaction_score,
    'Region': regions,
    'DeviceType': devices,
    'LoyaltyTier': loyalty_tier,
    'Churn': churn
})

ecommerce_df.to_csv('sample_datasets/ecommerce_customers.csv', index=False)
print(f"✅ E-Commerce Dataset: {ecommerce_df.shape[0]} customers, {ecommerce_df.shape[1]} features")
print(f"   - Regression Targets: TotalSpent, AvgOrderValue")
print(f"   - Classification Targets: LoyaltyTier (3 classes), Churn (binary)")
print(f"   - Clustering: Customer segmentation\n")

# ==========================================
# 2. EMPLOYEE SALARY & PERFORMANCE DATA
# ==========================================
print("Creating Employee Salary Dataset...")

n_employees = 400

# Experience (years) - realistic distribution
experience = np.random.gamma(5, 2, n_employees).clip(0, 30).round(1)

# Education level (categorical, affects salary)
education = np.random.choice(['Bachelor', 'Master', 'PhD'], n_employees, p=[0.50, 0.40, 0.10])
education_bonus = {'Bachelor': 0, 'Master': 15000, 'PhD': 30000}

# Department (categorical)
departments = np.random.choice(['IT', 'Sales', 'HR', 'Finance', 'Marketing'], n_employees, 
                              p=[0.30, 0.25, 0.15, 0.20, 0.10])
dept_base = {'IT': 70000, 'Sales': 60000, 'HR': 55000, 'Finance': 75000, 'Marketing': 65000}

# Job level (based on experience)
job_levels = []
for exp in experience:
    if exp < 2:
        job_levels.append('Junior')
    elif exp < 7:
        job_levels.append('Mid')
    elif exp < 15:
        job_levels.append('Senior')
    else:
        job_levels.append('Lead')

# Performance rating (1-5, influenced by experience)
performance = (3 + experience * 0.05 + np.random.normal(0, 0.4, n_employees)).clip(1.5, 5).round(1)

# Projects completed (related to experience and performance)
projects = (experience * 2 + performance * 3 + np.random.normal(0, 5, n_employees)).clip(1, 100).astype(int)

# Training hours (inversely related to experience initially, then increases for senior)
training_hours = []
for exp in experience:
    if exp < 2:
        base = 120
    elif exp < 7:
        base = 60
    elif exp < 15:
        base = 40
    else:
        base = 80  # seniors do leadership training
    training_hours.append(int(base + np.random.normal(0, 15)))

training_hours = np.array(training_hours).clip(20, 200)

# Salary - REGRESSION TARGET (realistic formula)
base_salary = np.array([dept_base[dept] for dept in departments])
edu_bonus = np.array([education_bonus[edu] for edu in education])

salary = (base_salary + 
         edu_bonus + 
         experience * 2500 +  # experience premium
         performance * 5000 +  # performance bonus
         projects * 200 +      # project bonus
         np.random.normal(0, 5000, n_employees))  # random variance

salary = salary.clip(40000, 200000).round(0)

# Bonus percentage (related to performance and salary)
bonus_pct = (performance * 3 + np.random.normal(5, 2, n_employees)).clip(0, 25).round(1)

# Work-life balance score (1-5)
work_life = (4 - experience * 0.05 + np.random.normal(0.5, 0.5, n_employees)).clip(1, 5).round(1)

# Promotion probability (classification) - binary
promotion = []
for i in range(n_employees):
    promo_prob = 0.1  # base rate
    if performance[i] > 4:
        promo_prob += 0.4
    if projects[i] > 20:
        promo_prob += 0.2
    if experience[i] > 3 and experience[i] < 15:  # sweet spot
        promo_prob += 0.2
    promotion.append(1 if np.random.random() < promo_prob else 0)

# Attrition risk (binary classification)
attrition = []
for i in range(n_employees):
    risk = 0.2
    if salary[i] < 60000:
        risk += 0.2
    if work_life[i] < 2.5:
        risk += 0.25
    if performance[i] < 3:
        risk += 0.15
    attrition.append(1 if np.random.random() < risk else 0)

employee_df = pd.DataFrame({
    'EmployeeID': range(1, n_employees + 1),
    'Experience': experience,
    'Education': education,
    'Department': departments,
    'JobLevel': job_levels,
    'PerformanceRating': performance,
    'ProjectsCompleted': projects,
    'TrainingHours': training_hours,
    'Salary': salary,
    'BonusPercentage': bonus_pct,
    'WorkLifeBalance': work_life,
    'Promotion': promotion,
    'Attrition': attrition
})

employee_df.to_csv('sample_datasets/employee_salaries.csv', index=False)
print(f"✅ Employee Dataset: {employee_df.shape[0]} employees, {employee_df.shape[1]} features")
print(f"   - Regression Target: Salary (realistic $40K-$200K)")
print(f"   - Classification Targets: Promotion (binary), Attrition (binary)")
print(f"   - Clustering: Employee segmentation by performance\n")

# ==========================================
# 3. STUDENT ACADEMIC PERFORMANCE
# ==========================================
print("Creating Student Performance Dataset...")

n_students = 600

# Study hours per week (realistic distribution)
study_hours = np.random.gamma(4, 2, n_students).clip(5, 40).round(1)

# Attendance percentage
attendance = np.random.beta(8, 2, n_students) * 100
attendance = attendance.clip(50, 100).round(1)

# Previous exam score (baseline ability)
previous_score = np.random.normal(70, 15, n_students).clip(30, 100).round(0)

# Parent education level (categorical, affects support)
parent_edu = np.random.choice(['High School', 'Bachelor', 'Master', 'PhD'], n_students, 
                             p=[0.30, 0.40, 0.20, 0.10])
parent_support = {'High School': 0, 'Bachelor': 5, 'Master': 8, 'PhD': 10}

# Extra classes (hours per week)
extra_classes = np.random.poisson(3, n_students).clip(0, 15)

# Assignment submission rate
assignment_rate = (attendance / 100 * 0.9 + np.random.normal(0, 0.1, n_students)).clip(0.4, 1.0).round(2)

# Participation score (1-10)
participation = (study_hours * 0.2 + attendance * 0.05 + np.random.normal(0, 1, n_students)).clip(1, 10).round(1)

# Internet access (binary)
internet = np.random.choice([0, 1], n_students, p=[0.15, 0.85])

# Final exam score - REGRESSION TARGET (realistic formula)
parent_bonus = np.array([parent_support[edu] for edu in parent_edu])

final_score = (previous_score * 0.3 +  # past performance
              study_hours * 1.2 +       # study impact
              attendance * 0.15 +       # attendance impact
              extra_classes * 0.8 +     # extra help
              assignment_rate * 15 +    # assignment completion
              participation * 1.5 +     # class participation
              parent_bonus +            # family support
              internet * 5 +            # internet access
              np.random.normal(0, 8, n_students))  # random factors

final_score = final_score.clip(30, 100).round(0)

# Grade category (classification) - based on final score
grades = []
for score in final_score:
    if score >= 90:
        grades.append('A')
    elif score >= 80:
        grades.append('B')
    elif score >= 70:
        grades.append('C')
    elif score >= 60:
        grades.append('D')
    else:
        grades.append('F')

# Pass/Fail (binary classification)
pass_fail = (final_score >= 60).astype(int)

# At-risk student (binary) - needs intervention
at_risk = []
for i in range(n_students):
    risk = 0.1
    if study_hours[i] < 10:
        risk += 0.3
    if attendance[i] < 75:
        risk += 0.25
    if assignment_rate[i] < 0.7:
        risk += 0.2
    at_risk.append(1 if np.random.random() < risk else 0)

# School type
school_type = np.random.choice(['Public', 'Private'], n_students, p=[0.70, 0.30])

student_df = pd.DataFrame({
    'StudentID': range(1, n_students + 1),
    'StudyHoursPerWeek': study_hours,
    'AttendancePercentage': attendance,
    'PreviousExamScore': previous_score,
    'ParentEducation': parent_edu,
    'ExtraClassesHours': extra_classes,
    'AssignmentSubmissionRate': assignment_rate,
    'ParticipationScore': participation,
    'InternetAccess': internet,
    'SchoolType': school_type,
    'FinalExamScore': final_score,
    'Grade': grades,
    'Pass': pass_fail,
    'AtRisk': at_risk
})

student_df.to_csv('sample_datasets/student_performance.csv', index=False)
print(f"✅ Student Dataset: {student_df.shape[0]} students, {student_df.shape[1]} features")
print(f"   - Regression Target: FinalExamScore (30-100)")
print(f"   - Classification Targets: Grade (A-F), Pass (binary), AtRisk (binary)")
print(f"   - Clustering: Student grouping by study patterns\n")

# ==========================================
# 4. REAL ESTATE PROPERTY PRICES
# ==========================================
print("Creating Real Estate Dataset...")

n_properties = 450

# Property size (square feet) - realistic distribution
size_sqft = np.random.gamma(8, 250, n_properties).clip(500, 5000).round(0)

# Number of bedrooms (correlated with size)
bedrooms = []
for size in size_sqft:
    if size < 1000:
        bed = np.random.choice([1, 2], p=[0.6, 0.4])
    elif size < 1500:
        bed = np.random.choice([2, 3], p=[0.5, 0.5])
    elif size < 2500:
        bed = np.random.choice([3, 4], p=[0.6, 0.4])
    else:
        bed = np.random.choice([4, 5], p=[0.7, 0.3])
    bedrooms.append(bed)

bedrooms = np.array(bedrooms)

# Bathrooms (correlated with bedrooms)
bathrooms = (bedrooms * 0.75 + np.random.choice([0, 0.5, 1], n_properties)).clip(1, 4).round(1)

# Property age (years)
property_age = np.random.exponential(15, n_properties).clip(0, 50).astype(int)

# Location rating (1-10, affects price significantly)
location_rating = np.random.beta(6, 3, n_properties) * 10
location_rating = location_rating.clip(3, 10).round(1)

# Distance to city center (km)
distance_center = np.random.exponential(8, n_properties).clip(1, 40).round(1)

# Crime rate (per 1000, inversely related to location rating)
crime_rate = (15 - location_rating * 1.2 + np.random.normal(0, 2, n_properties)).clip(2, 20).round(1)

# School rating nearby (1-10)
school_rating = (location_rating * 0.7 + np.random.normal(2, 1, n_properties)).clip(3, 10).round(1)

# Has parking (binary)
parking = np.random.choice([0, 1], n_properties, p=[0.25, 0.75])

# Has garden (binary, more common in larger properties)
garden = []
for size in size_sqft:
    prob = 0.3 if size < 1500 else 0.7
    garden.append(np.random.choice([0, 1], p=[1-prob, prob]))

garden = np.array(garden)

# Recently renovated (binary, less likely for older properties)
renovated = []
for age in property_age:
    prob = 0.4 if age < 10 else 0.15
    renovated.append(np.random.choice([0, 1], p=[1-prob, prob]))

renovated = np.array(renovated)

# Neighborhood (categorical)
neighborhoods = np.random.choice(['Downtown', 'Suburbs', 'Rural', 'Waterfront', 'Historic'], 
                                n_properties, p=[0.25, 0.40, 0.15, 0.12, 0.08])
neighborhood_premium = {
    'Downtown': 100000, 
    'Suburbs': 50000, 
    'Rural': 0, 
    'Waterfront': 150000, 
    'Historic': 80000
}

# Property price - REGRESSION TARGET (realistic formula)
base_price = 50000
size_value = size_sqft * 150  # $150 per sqft
location_value = location_rating * 25000
school_value = school_rating * 15000
age_depreciation = property_age * 2000
neighborhood_value = np.array([neighborhood_premium[n] for n in neighborhoods])

price = (base_price + 
        size_value + 
        location_value + 
        school_value - 
        age_depreciation + 
        neighborhood_value +
        parking * 20000 +
        garden * 30000 +
        renovated * 40000 +
        bedrooms * 25000 +
        np.random.normal(0, 30000, n_properties))

price = price.clip(100000, 1500000).round(-3)  # round to nearest 1000

# Price category (classification)
price_category = []
for p in price:
    if p < 300000:
        price_category.append('Budget')
    elif p < 600000:
        price_category.append('Mid-Range')
    elif p < 900000:
        price_category.append('Upscale')
    else:
        price_category.append('Luxury')

# Investment potential (binary) - good for flipping
investment = []
for i in range(n_properties):
    score = 0
    if location_rating[i] > 7:
        score += 2
    if property_age[i] > 20 and not renovated[i]:
        score += 2  # renovation potential
    if distance_center[i] < 10:
        score += 1
    if price[i] < 400000:
        score += 1
    investment.append(1 if score >= 4 else 0)

realestate_df = pd.DataFrame({
    'PropertyID': range(1, n_properties + 1),
    'SizeSquareFeet': size_sqft,
    'Bedrooms': bedrooms,
    'Bathrooms': bathrooms,
    'PropertyAge': property_age,
    'LocationRating': location_rating,
    'DistanceToCityCenter': distance_center,
    'CrimeRate': crime_rate,
    'SchoolRating': school_rating,
    'Parking': parking,
    'Garden': garden,
    'RecentlyRenovated': renovated,
    'Neighborhood': neighborhoods,
    'Price': price,
    'PriceCategory': price_category,
    'InvestmentPotential': investment
})

realestate_df.to_csv('sample_datasets/real_estate_prices.csv', index=False)
print(f"✅ Real Estate Dataset: {realestate_df.shape[0]} properties, {realestate_df.shape[1]} features")
print(f"   - Regression Target: Price ($100K-$1.5M)")
print(f"   - Classification Targets: PriceCategory (4 classes), InvestmentPotential (binary)")
print(f"   - Clustering: Property segmentation\n")

print("="*60)
print("✅ ALL DATASETS CREATED SUCCESSFULLY!")
print("="*60)
print("\n📊 Dataset Summary:\n")
print("1. ecommerce_customers.csv - E-commerce customer behavior")
print("   Perfect for: All algorithms, customer segmentation")
print()
print("2. employee_salaries.csv - Employee performance & compensation")
print("   Perfect for: Salary prediction, promotion forecasting")
print()
print("3. student_performance.csv - Academic achievement analysis")
print("   Perfect for: Score prediction, at-risk student identification")
print()
print("4. real_estate_prices.csv - Property pricing analysis")
print("   Perfect for: Price prediction, investment opportunity detection")
print()
print("🎯 All datasets have:")
print("   ✅ Meaningful relationships between features")
print("   ✅ Realistic patterns and distributions")
print("   ✅ Multiple targets for regression AND classification")
print("   ✅ Good for clustering analysis")
print("   ✅ Perfect for professional demos!")
