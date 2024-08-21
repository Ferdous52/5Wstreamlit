import streamlit as st
import pandas as pd

st.set_page_config()

# Initialize session state for login
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Define a function for the login page
def login():
    st.markdown(
        """
        <style>
        .login-container {
            background-color: #f2f2f2;
            padding: 50px;
            border-radius: 10px;
            box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.1);
            max-width: 400px;
            margin: auto;
        }
        .login-title {
            font-size: 30px;
            text-align: center;
            margin-bottom: 20px;
            color: #333333;
        }
        .login-input {
            margin-bottom: 10px;
        }
        .login-button {
            background-color: #4CAF50;
            color: white;
            width: 100%;
            padding: 10px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 18px;
        }
        .login-button:hover {
            background-color: #45a049;
        }
        </style>
        """, unsafe_allow_html=True
    )

    st.markdown('<div class="login-container">', unsafe_allow_html=True)

    st.markdown('<div class="login-title">Login</div>', unsafe_allow_html=True)

    username = st.text_input("Username", placeholder="Enter your username", key="username",
                             label_visibility="collapsed", help="Enter your username here")
    password = st.text_input("Password", type="password", placeholder="Enter your password", key="password",
                             label_visibility="collapsed", help="Enter your password here")

    if st.button("Login", help="Click to login", use_container_width=True, key="login_button"):
        if username == "ferdous" and password == "123":
            st.session_state.logged_in = True
        else:
            st.error("Invalid username or password. Please try again.")

    st.markdown('</div>', unsafe_allow_html=True)

# Define a function for the logout page
def logout():
    st.session_state.logged_in = False
    st.success("You have successfully logged out.")

# Define the main app after login
def app():
    st.title("5W Data Management")

    # Logout button in the sidebar
    if st.sidebar.button("Logout"):
        logout()

    # Option to select between 5W data comparison and 5W analysis
    st.write("### Select an Option")
    option = st.selectbox("", ["Select an option", "5W data Comparison", "5W analysis"])

    if option == "5W data Comparison":
        st.write("## 5W Data Comparison")



        # File uploader for two Excel files
        file1 = st.file_uploader("Upload the first 5W data file", type=["xlsx"], key="file1")
        file2 = st.file_uploader("Upload the second 5W data file", type=["xlsx"], key="file2")

        if file1 and file2:
            try:

                df1 = pd.read_excel(file1, sheet_name='5W_Enrollment', skiprows=2, engine='openpyxl')
                df2 = pd.read_excel(file2, sheet_name='5W_Enrollment', skiprows=2, engine='openpyxl')

                # Add your comparison logic here

                st.success("Files uploaded successfully. Ready for comparison.")
            except Exception as e:
                st.error(f"Error reading files: {e}")

    elif option == "5W analysis":
        st.write("## 5W Analysis")

        # File uploader for a single Excel file
        file1 = st.file_uploader("Upload the 5W data", type=["xlsx"])


        if file1 is not None:
            try:
                bytes_data = file1.getvalue()
                df1 = pd.read_excel(bytes_data, sheet_name='5W_Enrollment', skiprows=2)
                df1 = df1.dropna(subset=['Facility ID'])

                # Cleaned and structured dataframes
                Facility_info = df1[['Camp/Union', 'Block Name/ Ward for Host', 'Latitude', 'Longitude', 'Sub-Block',
                                     'Facility Name', 'Facility ID', 'Facility Type', 'Intervention']]

                Enrollment = df1[['Camp/Union', 'Facility Name', 'Facility ID', 'Facility Type',
                                  'Shift',
                                  'Girls only ssession',
                                  'Age Group',
                                  'Intervention',
                                  '# of Girls (Including CwD)',
                                  '# of Girls with Disability',
                                  '# of Boys (Including CwD)',
                                  '# of Boys with Disability',
                                  'Total', ]]

                Attendance = df1[['Camp/Union', 'Facility Name', 'Facility ID', 'Facility Type', 'Intervention',
                                  '# of Girls Attended_Reg',
                                  '# of Boys Attended_Reg',
                                  'Total Attended_Reg',
                                  '# of Girls Attended_Irreg',
                                  '# of Boys Attended_Irreg',
                                  'Total Attended_Irreg',
                                  '# of Girls Attended_S_Irreg',
                                  '# of Boys Attended_S_Irreg',
                                  'Total Attended_S_Irreg']]

                Dropout = df1[['Camp/Union', 'Facility Name', 'Facility ID', 'Facility Type', 'Intervention',
                               'Girls_Drop',
                               'Boys_Drop',
                               'Total_Drop']]

                LF_move = df1[['Camp/Union', 'Facility Name', 'Facility ID', 'Facility Type',
                               'Girls_Move_LF',
                               'Boys_Move_LF',
                               'Total_Move_LF']]

                Camp_move = df1[['Camp/Union', 'Facility Name', 'Facility ID', 'Facility Type',
                                 'Girls_Move_Camp',
                                 'Boys_Move_Camp',
                                 'Total_Move_Camp']]
                phv = df1[['Camp/Union', 'Facility Name', 'Facility ID', 'Facility Type',
                           'Girls_PhV',
                           'Boys_PhV',
                           'Total_PhV']]

                Facilitators = df1[['Camp/Union', 'Facility Name', 'Facility ID', 'Facility Type',
                                    'HC Female Teachers/ Facilitators',
                                    'HC Male Teachers/ Facilitators',
                                    'RC Female Rohingya Facilitators/ Teachers',
                                    'RC Male Rohingya Facilitators/ Teachers']]

                Volunteers = df1[['Camp/Union', 'Facility Name', 'Facility ID', 'Facility Type',
                                  'HC Female Volunteers/ Guards',
                                  'HC Male Volunteers/ Guards',
                                  'RC Female Volunteers/ Guards',
                                  'RC Male Volunteers/ Guards']]

                cwd = df1[['Camp/Union', 'Facility Name', 'Facility ID', 'Facility Type', 'Intervention',
                           'Girls_CwD',
                           'Boys_CwD',
                           'Total_CwD']]

                Current_learners = df1[['Camp/Union', 'Facility Name', 'Facility ID', 'Facility Type', 'Intervention',
                                        'Girls',
                                        'Boys',
                                        'Total learners']]

                Attendance_check = df1[['Camp/Union', 'Facility Name', 'Facility ID', 'Facility Type',
                                        'Girls_check',
                                        'Boys_Check']]
                variables_dict = {

                    "Enrollment": Enrollment,
                    "Attendance": Attendance,
                    "Dropout": Dropout,
                    "LF_move": LF_move,
                    "Camp_move": Camp_move,
                    "phv": phv,
                    "Facilitators": Facilitators,
                    "Volunteers": Volunteers,
                    "cwd": cwd,
                    "Current_learners": Current_learners,
                    "Attendance_check": Attendance_check
                }


                # Facility Information Section
                st.write("## Facility Information")
                with st.expander("Show Facility Information"):
                    st.dataframe(Facility_info)

                # Pivot Table Section
                pivot_table1 = pd.pivot_table(
                    Facility_info,
                    values='Facility ID',
                    index='Camp/Union',
                    columns=['Facility Type'],
                    aggfunc='nunique',
                    fill_value=0,
                    margins=True,
                    margins_name='Total')

                st.dataframe(pivot_table1, use_container_width=True)

                st.write("#### Camp-wise Facility Type")
                pivot_table2 = pd.pivot_table(
                    Facility_info,
                    values='Facility ID',
                    index='Camp/Union',
                    columns=['Intervention'],
                    aggfunc='nunique',
                    fill_value=0,
                    margins=True,
                    margins_name='Total')

                st.dataframe(pivot_table2, use_container_width=True)
                st.write("#### Number of Intervention wise Facility")
                pivot_table3 = pd.pivot_table(
                    Facility_info,
                    values='Facility ID',
                    index='Intervention',
                    columns=['Facility Type'],
                    aggfunc='nunique',
                    fill_value=0,
                    margins=True,
                    margins_name='Total')

                st.dataframe(pivot_table3, use_container_width=True, height=530)

                # User selects a variable to analyze
                st.write("##### Select a variable to analyze")
                selected_variable = st.selectbox("", list(variables_dict.keys()))

                if selected_variable:
                    #st.write(f"### Data of {selected_variable}")
                    selected_df = variables_dict[selected_variable]

                    # Hidden DataFrame for the selected variable
                    with st.expander(f"Show {selected_variable} Data"):
                        st.dataframe(selected_df)

                    # Pivot Table for the selected variable
                    st.write("#### Pivot Table of", selected_variable)
                    if selected_variable == selected_variable:
                        index_columns = 'Camp/Union'
                        numeric_columns = selected_df.select_dtypes(include='number').columns
                        value_columns = st.multiselect("Select value columns for the pivot table", numeric_columns)
                        if value_columns:
                            pivot_table = pd.pivot_table(
                                selected_df,
                                values=value_columns,
                                index=[index_columns],
                                aggfunc='sum',
                                fill_value=0,
                                margins=True,
                                margins_name='Total'
                            )

                            st.write(pivot_table)
                            pivot_table = pivot_table.drop('Total')
                            st.write("#### Visualization of", selected_variable)
                            st.bar_chart(pivot_table, height=400)

            except Exception as e:
                st.error(f"Error reading file: {e}")

# Show login page or main app based on login status
if not st.session_state.logged_in:
    login()
else:
    app()
