import streamlit as st
import pandas as pd

# Streamlit app configuration
st.set_page_config(page_title="Tax Regime Comparison FY 2025-26", layout="wide")

# Title and description
st.title("Tax Regime Comparison FY 2025-26")
st.markdown("Compare your tax liability under the Old and New Tax Regimes. Enter your details below:")

# Default tax slabs
default_old_slabs = [
    {"range": "0L - 2.5L", "rate": 0.0, "lower": 0, "upper": 250000},
    {"range": "2.5L - 5L", "rate": 0.05, "lower": 250000, "upper": 500000},
    {"range": "5L - 10L", "rate": 0.2, "lower": 500000, "upper": 1000000},
    {"range": "10L - 21.95L", "rate": 0.3, "lower": 1000000, "upper": 2195000},
    {"range": "Above 21.95L", "rate": 0.3, "lower": 2195000, "upper": float("inf")}
]

default_new_slabs = [
    {"range": "0L - 3L", "rate": 0.0, "lower": 0, "upper": 300000},
    {"range": "3L - 6L", "rate": 0.05, "lower": 300000, "upper": 600000},
    {"range": "6L - 9L", "rate": 0.1, "lower": 600000, "upper": 900000},
    {"range": "9L - 12L", "rate": 0.15, "lower": 900000, "upper": 1200000},
    {"range": "12L - 15L", "rate": 0.2, "lower": 1200000, "upper": 1500000},
    {"range": "15L - 27.57L", "rate": 0.25, "lower": 1500000, "upper": 2757000},
    {"range": "Above 27.57L", "rate": 0.3, "lower": 2757000, "upper": float("inf")}
]

# Default standard deductions
default_standard_deduction_old = 50000
default_standard_deduction_new = 75000

# Function to create a tooltip
def add_tooltip(label, tooltip_text):
    return st.markdown(f"""
        {label} <span style='cursor: pointer; color: blue;' title='{tooltip_text}'>[?]</span>
    """, unsafe_allow_html=True)

# Input fields for user variables
st.header("Input Your Details")
col1, col2 = st.columns(2)

with col1:
    add_tooltip("Gross Annual Salary (₹)", 
                "Your total annual salary before any deductions or exemptions.")
    salary = st.number_input("", min_value=0.0, value=3000000.0, step=10000.0, key="salary")

    add_tooltip("HRA/Home Loan Exemption (₹)", 
                "HRA exemption is available under the old regime for salaried individuals paying rent. "
                "It is the least of: actual HRA received, rent paid minus 10% of salary, or 50% of salary (metro cities) / 40% (non-metro). "
                "Learn more: https://cleartax.in/s/hra-house-rent-allowance")
    hra_exemption = st.number_input("", min_value=0.0, value=360000.0, step=1000.0, key="hra")

with col2:
    add_tooltip("80C Deduction (₹)", 
                "Allows a deduction of up to ₹1,50,000 for investments in specified instruments like PPF, EPF, "
                "life insurance premiums, ELSS, and tuition fees. "
                "Learn more: https://incometaxindia.gov.in/Pages/Acts/Section-80C.aspx")
    deductions_80c = st.number_input("", min_value=0.0, max_value=150000.0, value=150000.0, step=1000.0, key="80c")

    add_tooltip("80D Deduction (₹)", 
                "Provides a deduction for health insurance premiums paid for self, family, or parents. "
                "The limit is ₹25,000 for self/family and an additional ₹50,000 for senior citizen parents. "
                "Learn more: https://www.etmoney.com/learn/income-tax/section-80d-deduction-for-medical-insurance-premium/")
    deductions_80d = st.number_input("", min_value=0.0, max_value=75000.0, value=75000.0, step=1000.0, key="80d")

    add_tooltip("80CCD(1B) Deduction (₹)", 
                "Offers an additional deduction of up to ₹50,000 for contributions to the National Pension System (NPS) "
                "over and above the 80C limit. "
                "Learn more: https://tax2win.in/guide/section-80ccd")
    deductions_80ccd1b = st.number_input("", min_value=0.0, max_value=50000.0, value=50000.0, step=1000.0, key="80ccd1b")

# Input for standard deductions
st.header("Standard Deductions (Leave as 0 to use defaults)")
col3, col4 = st.columns(2)

with col3:
    add_tooltip("Standard Deduction - Old Regime (₹)", 
                "A fixed deduction allowed from gross salary to reduce taxable income. "
                "Default for FY 2025-26 is ₹50,000 in the old regime. "
                "Learn more: https://incometaxindia.gov.in/Pages/FAQs/Standard-deduction.aspx")
    standard_deduction_old = st.number_input("", min_value=0.0, value=0.0, step=1000.0, key="std_old")
    st.write(f"Default: ₹{default_standard_deduction_old:,.2f}")

with col4:
    add_tooltip("Standard Deduction - New Regime (₹)", 
                "A fixed deduction allowed from gross salary to reduce taxable income. "
                "Default for FY 2025-26 is ₹75,000 in the new regime. "
                "Learn more: https://incometaxindia.gov.in/Pages/FAQs/Standard-deduction.aspx")
    standard_deduction_new = st.number_input("", min_value=0.0, value=0.0, step=1000.0, key="std_new")
    st.write(f"Default: ₹{default_standard_deduction_new:,.2f}")

# Use default standard deductions if user inputs 0
standard_deduction_old = default_standard_deduction_old if standard_deduction_old == 0 else standard_deduction_old
standard_deduction_new = default_standard_deduction_new if standard_deduction_new == 0 else standard_deduction_new

# Input for tax slabs (allowing users to override defaults)
st.header("Custom Tax Slabs (Optional)")
st.markdown("Define custom tax slabs below. Leave blank to use defaults.")

# Old Regime Slabs Input
st.subheader("Old Regime Tax Slabs")
add_tooltip("Old Regime Tax Slabs", 
            "Tax slabs define the income ranges and corresponding tax rates under the old regime. "
            "You can customize these slabs or use the defaults for FY 2025-26. "
            "Learn more: https://incometaxindia.gov.in/Pages/tools/tax-calculator.aspx")
old_slabs = []
for i in range(5):  # Allow up to 5 slabs
    col5, col6, col7 = st.columns(3)
    with col5:
        lower = st.number_input(f"Old Slab {i+1} - Lower Limit (₹)", min_value=0.0, value=0.0, step=10000.0, key=f"old_lower_{i}")
    with col6:
        upper = st.number_input(f"Old Slab {i+1} - Upper Limit (₹, use 0 for infinity)", min_value=0.0, value=0.0, step=10000.0, key=f"old_upper_{i}")
    with col7:
        rate = st.number_input(f"Old Slab {i+1} - Tax Rate (%)", min_value=0.0, max_value=100.0, value=0.0, step=0.1, key=f"old_rate_{i}")
    if lower != 0 or upper != 0 or rate != 0:
        upper = float("inf") if upper == 0 else upper
        old_slabs.append({"lower": lower, "upper": upper, "rate": rate / 100})

# New Regime Slabs Input
st.subheader("New Regime Tax Slabs")
add_tooltip("New Regime Tax Slabs", 
            "Tax slabs define the income ranges and corresponding tax rates under the new regime. "
            "You can customize these slabs or use the defaults for FY 2025-26. "
            "Learn more: https://incometaxindia.gov.in/Pages/tools/tax-calculator.aspx")
new_slabs = []
for i in range(7):  # Allow up to 7 slabs (as per new regime structure)
    col8, col9, col10 = st.columns(3)
    with col8:
        lower = st.number_input(f"New Slab {i+1} - Lower Limit (₹)", min_value=0.0, value=0.0, step=10000.0, key=f"new_lower_{i}")
    with col9:
        upper = st.number_input(f"New Slab {i+1} - Upper Limit (₹, use 0 for infinity)", min_value=0.0, value=0.0, step=10000.0, key=f"new_upper_{i}")
    with col10:
        rate = st.number_input(f"New Slab {i+1} - Tax Rate (%)", min_value=0.0, max_value=100.0, value=0.0, step=0.1, key=f"new_rate_{i}")
    if lower != 0 or upper != 0 or rate != 0:
        upper = float("inf") if upper == 0 else upper
        new_slabs.append({"lower": lower, "upper": upper, "rate": rate / 100})

# Use default slabs if user doesn't provide custom slabs
old_slabs = default_old_slabs if not old_slabs else old_slabs
new_slabs = default_new_slabs if not new_slabs else new_slabs

# Display default tax slabs
st.subheader("Default Tax Slabs (Used if custom slabs are not provided)")
col11, col12 = st.columns(2)
with col11:
    st.write("**Old Regime Default Slabs**")
    for slab in default_old_slabs:
        st.write(f"{slab['range']}: {slab['rate']*100}%")
with col12:
    st.write("**New Regime Default Slabs**")
    for slab in default_new_slabs:
        st.write(f"{slab['range']}: {slab['rate']*100}%")

# Function to calculate tax under both regimes
def calculate_tax(salary, hra_exemption, deductions_80c, deductions_80d, deductions_80ccd1b, standard_deduction_old, standard_deduction_new, old_slabs, new_slabs):
    # Step 1: Gross Income Calculation
    net_salary_old = salary - standard_deduction_old
    net_salary_new = salary - standard_deduction_new
    
    gross_total_old = net_salary_old - hra_exemption
    gross_total_new = net_salary_new  # No HRA exemption in new regime
    
    # Step 2: Deductions
    basic_salary = salary * 0.4  # Assuming 40% of salary is basic
    deduction_80ccd2_new = basic_salary * 0.1  # 10% of basic salary for 80CCD(2) in new regime
                # Tooltip for 80CCD(2) in the note below
    
    total_deductions_old = deductions_80c + deductions_80d + deductions_80ccd1b
    total_deductions_new = deduction_80ccd2_new
    
    total_income_old = gross_total_old - total_deductions_old
    total_income_new = gross_total_new - total_deductions_new
    
    # Step 3: Tax Calculation - Old Regime
    tax_old = 0
    for slab in old_slabs:
        if total_income_old > slab["lower"]:
            taxable_in_slab = min(slab["upper"] - slab["lower"], max(0, total_income_old - slab["lower"]))
            tax_old += taxable_in_slab * slab["rate"]
    
    # Step 4: Tax Calculation - New Regime
    tax_new = 0
    for slab in new_slabs:
        if total_income_new > slab["lower"]:
            taxable_in_slab = min(slab["upper"] - slab["lower"], max(0, total_income_new - slab["lower"]))
            tax_new += taxable_in_slab * slab["rate"]
    
    # Step 5: Add 4% Health and Education Cess
    cess_old = tax_old * 0.04
    cess_new = tax_new * 0.04
    
    total_tax_old = tax_old + cess_old
    total_tax_new = tax_new + cess_new
    
    return total_tax_old, total_tax_new, total_income_old, total_income_new, total_deductions_old, total_deductions_new

# Calculate tax based on user inputs
total_tax_old, total_tax_new, total_income_old, total_income_new, total_deductions_old, total_deductions_new = calculate_tax(
    salary, hra_exemption, deductions_80c, deductions_80d, deductions_80ccd1b, standard_deduction_old, standard_deduction_new, old_slabs, new_slabs
)

# Step 6: Display Results
st.header("Tax Calculation Results")

# Create a DataFrame for displaying results
results = {
    "Description": [
        "Gross Salary (₹)",
        "Standard Deduction (₹)",
        "HRA Exemption (₹)",
        "Total Deductions (₹)",
        "Taxable Income (₹)",
        "Total Tax (₹)"
    ],
    "Old Regime": [
        f"{salary:,.2f}",
        f"{standard_deduction_old:,.2f}",
        f"{hra_exemption:,.2f}",
        f"{total_deductions_old:,.2f}",
        f"{total_income_old:,.2f}",
        f"{total_tax_old:,.2f}"
    ],
    "New Regime": [
        f"{salary:,.2f}",
        f"{standard_deduction_new:,.2f}",
        "0.00",
        f"{total_deductions_new:,.2f}",
        f"{total_income_new:,.2f}",
        f"{total_tax_new:,.2f}"
    ]
}

df = pd.DataFrame(results)
st.table(df)

# Display Difference and Recommendation
difference = total_tax_old - total_tax_new
st.subheader("Comparison")
st.write(f"**Difference (Old - New)**: ₹{difference:,.2f}")
st.write(f"**Recommendation**: {'New Regime' if difference > 0 else 'Old Regime'} is more beneficial.")

# Add a note with tooltip for 80CCD(2)
st.markdown("""
    **Note**: The 80CCD(2) deduction in the new regime is calculated as 10% of basic salary (assumed 40% of gross salary).
    <span style='cursor: pointer; color: blue;' title='80CCD(2) allows a deduction for the employer’s contribution to the employee’s NPS account, up to 10% of salary (basic + DA). This is available in both old and new regimes. Learn more: https://cleartax.in/s/section-80ccd'>[?]</span>
""", unsafe_allow_html=True)