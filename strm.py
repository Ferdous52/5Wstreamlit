import streamlit as st
import pandas as pd


st.set_page_config(page_title="5W")

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

    username = st.text_input("Username", placeholder="Enter your username", key="username",label_visibility="collapsed", help="Enter your username here")
    password = st.text_input("Password", type="password", placeholder="Enter your password", key="password",label_visibility="collapsed", help="Enter your password here")

    if st.button("Login", help="Click to login", use_container_width=True, key="login_button"):
        if username == "dipu" and password == "01516":
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

    option = st.selectbox("", ["Select an option", "5W data Comparison", "5W analysis"])

    if option == "5W data Comparison":
        st.write("## 5W Data Comparison")

        # File uploader for two Excel files
        file1 = st.file_uploader("Upload the Previous Month 5W data file", type=["xlsx"], key="file1")
        file2 = st.file_uploader("Upload the Current Month 5W data file", type=["xlsx"], key="file2")

        if file1 and file2:
            try:
                st.write("Previous Month 5W")
                df1 = pd.read_excel(file1, sheet_name='5W_Enrollment', skiprows=2, engine='openpyxl')
                df1 = df1.dropna(subset=['Facility ID'])
                with st.expander("Show the data"):
                    st.dataframe(df1)
                st.write("Current Month 5W")
                df2 = pd.read_excel(file2, sheet_name='5W_Enrollment', skiprows=2, engine='openpyxl')
                df2 = df2.dropna(subset=['Facility ID'])
                with st.expander("Show the data"):
                    st.dataframe(df2)

                # Columns to compare
                comparison_columns = ['Camp/Union', 'Facility ID', 'Facility Type', 'Intervention']
                enroll_columns = ['# of Girls (Including CwD)', '# of Girls with Disability',
                                      '# of Boys (Including CwD)', '# of Boys with Disability', 'Total']

                 # Filter dataframes by comparison columns and enrollment columns
                df1_filtered = df1[comparison_columns + enroll_columns]
                df2_filtered = df2[comparison_columns + enroll_columns]

                # Merge the two dataframes on the comparison columns
                merged_df = pd.merge(df1_filtered, df2_filtered, on=comparison_columns, how='outer',
                                         suffixes=('_prev', '_curr'))

                # Calculate differences for numeric columns
                for col in enroll_columns:
                    merged_df[f'{col}_diff'] = merged_df[f'{col}_curr'] - merged_df[f'{col}_prev']

                # Filter the dataframe to show only rows with differences
                diff_df = merged_df[(merged_df[[f'{col}_diff' for col in enroll_columns]] != 0).any(axis=1)]

                # Display results
                st.write("### Enrollment Differences")
                if not diff_df.empty:
                    st.dataframe(diff_df)
                else:
                    st.write("No differences found in the numeric enrollment data.")

            except Exception as e:
                st.error(f"Error reading files: {e}")

    elif option == "5W analysis":
        st.write("## 5W Analysis")

        # File uploader for a single Excel file
        file1 = st.file_uploader("Upload the 5W data")


        if file1 is not None:
            try:

                df1 = pd.read_excel(file1, sheet_name='5W_Enrollment', skiprows=2)
                df1 = df1.dropna(subset=['Facility ID'])

                # Cleaned and structured dataframes for 5W Analysis
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

                Attendance = df1[['Camp/Union', 'Facility Name', 'Facility ID', 'Facility Type', 'Intervention','Shift',
                                  '# of Girls Attended_Reg',
                                  '# of Boys Attended_Reg',
                                  'Total Attended_Reg',
                                  '# of Girls Attended_Irreg',
                                  '# of Boys Attended_Irreg',
                                  'Total Attended_Irreg',
                                  '# of Girls Attended_S_Irreg',
                                  '# of Boys Attended_S_Irreg',
                                  'Total Attended_S_Irreg']]

                Dropout = df1[['Camp/Union', 'Facility Name', 'Facility ID', 'Facility Type', 'Intervention','Shift',
                               'Girls_Drop',
                               'Boys_Drop',
                               'Total_Drop']]

                LF_move = df1[['Camp/Union', 'Facility Name', 'Facility ID', 'Facility Type','Intervention',
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
                with st.expander("Show the data"):
                    #st.dataframe(Facility_info)
                    st.text('Camp-wise Facility Type')
                    # Pivot Table1  Section
                    pivot_table1 = pd.pivot_table(
                        Facility_info,
                        values='Facility ID',
                        index='Camp/Union',
                        columns=['Facility Type'],
                        aggfunc='nunique',
                        fill_value=0,
                        margins=True,
                        margins_name='Total')
                    st.dataframe(pivot_table1.style.format("{:.0f}"),use_container_width=True)

                    # Pivot Table3  Section
                    st.text("Intervention-wise Facility")
                    pivot_table3 = pd.pivot_table(
                        Facility_info,
                        values='Facility ID',
                        index='Intervention',
                        columns=['Facility Type'],
                        aggfunc='nunique',
                        fill_value=0,
                        margins=True,
                        margins_name='Total')
                    st.dataframe(pivot_table3,height=530,use_container_width= True)

                    # Create the pivot table
                    Facility_info['Facility Type'] = Facility_info['Facility Type'].replace({
                        'Learning Centre': 'LC',
                        'Community Based Learning Facility': 'CBLF'
                    })

                    pivot_table4 = pd.pivot_table(
                        Facility_info,
                        values='Facility ID',
                        index=['Facility Type', 'Intervention'],
                        columns='Camp/Union',
                        aggfunc='nunique',
                        fill_value=0,
                        margins=True,
                        margins_name='Total'
                    )

                    st.text("Total Facility Information")
                    st.dataframe(pivot_table4.style.format("{:.0f}"),height=702,use_container_width=True)


                st.write("## Enrollment")

                with st.expander("Show the data"):
                      Enrollment['Facility Type'] = Enrollment['Facility Type'].replace({
                            'Learning Centre': 'LC',
                            'Community Based Learning Facility': 'CBLF'})


                      Enrollment = Enrollment.rename(columns={'Camp/Union': 'Camp',
                                                             '# of Girls (Including CwD)':'Girls (Including CwD)',
                                                             '# of Girls with Disability':'Girls with Disability',
                                                             '# of Boys (Including CwD)':'Boys (Including CwD)',
                                                             '# of Boys with Disability': 'Boys with Disability'
                                                             })
                      Enrollment[['Girls (Including CwD)', 'Girls with Disability','Boys (Including CwD)','Boys with Disability','Total']] = Enrollment[
                         ['Girls (Including CwD)', 'Girls with Disability','Boys (Including CwD)', 'Boys with Disability','Total']].fillna(0)
                      pivot_enroll = pd.pivot_table(
                        Enrollment,
                        values=['Girls (Including CwD)',
                                  'Girls with Disability',
                                  'Boys (Including CwD)',
                                  'Boys with Disability',
                                  'Total'],
                        index='Camp',
                        aggfunc='sum',
                        fill_value='NaNs',
                        margins=True,
                        margins_name='Total')
                      st.dataframe(pivot_enroll, height=290,use_container_width=True)

                      pivot_enroll2 = pd.pivot_table(
                         Enrollment,
                         values=['Girls (Including CwD)',
                                 'Girls with Disability',
                                 'Boys (Including CwD)',
                                 'Boys with Disability',
                                 'Total'],
                         index=['Facility Type','Intervention'],
                         aggfunc='sum',
                         fill_value='0',
                         margins=True,
                         margins_name='Total')
                      st.dataframe(pivot_enroll2, height=705,use_container_width=True)


                st.write('## Current_learners')
                with st.expander('Show the data'):
                    Current_learners[['Girls','Boys','Total learners']]=Current_learners[['Girls','Boys','Total learners']].fillna(0)
                    pivot_cl = pd.pivot_table(
                        Current_learners,
                        values=[
                            'Girls',
                            'Boys',
                             'Total learners'],
                        index='Camp/Union',
                        aggfunc='sum',
                        fill_value=0,
                        margins=True,
                        margins_name='Total')
                    st.dataframe(pivot_cl, use_container_width=True)

                st.write("## Attendance")

                with st.expander("Show the data"):
                    Attendance = Attendance.rename(columns={'Camp/Union': 'Camp',
                                                            '# of Girls Attended_Reg': 'Girls Attended_Reg',
                                                            '# of Boys Attended_Reg': 'Boys Attended_Reg',
                                                            'Total Attended_Reg': 'Total Attended_Reg',
                                                            '# of Girls Attended_Irreg': 'Girls Attended_Irreg',
                                                            '# of Boys Attended_Irreg':'Boys Attended_Irreg',
                                                            'Total Attended_Irreg':'Total Attended_Irreg',
                                                            '# of Girls Attended_S_Irreg':'Girls Attended_S_Irreg',
                                                            '# of Boys Attended_S_Irreg':'Boys Attended_S_Irreg',
                                                            'Total Attended_S_Irreg':'Total Attended_S_Irreg'
                                                            })
                    Attendance[['Girls Attended_Reg','Boys Attended_Reg','Total Attended_Reg']]=Attendance[['Girls Attended_Reg','Boys Attended_Reg','Total Attended_Reg']].fillna(0)
                    st.text('Regular Attendance(above 80 %)')
                    pivot_attend_reg = pd.pivot_table(
                        Attendance,
                        values=['Girls Attended_Reg',
                                'Boys Attended_Reg',
                                'Total Attended_Reg'],
                        index='Camp',
                        aggfunc='sum',
                        fill_value=0,
                        margins=True,
                        margins_name='Total')
                    st.dataframe(pivot_attend_reg,use_container_width=True)

                    st.text('Irregular Attendance (51% to 79%)')
                    pivot_attend_Irreg = pd.pivot_table(
                        Attendance,
                        values=[
                                'Girls Attended_Irreg',
                                'Boys Attended_Irreg',
                                'Total Attended_Irreg',
                                ],
                        index='Camp',
                        aggfunc='sum',
                        fill_value=0,
                        margins=True,
                        margins_name='Total')
                    st.dataframe(pivot_attend_Irreg,use_container_width=True)

                    st.text('Severe Irregular Attendance(<50%)')
                    pivot_attend_s_ireg = pd.pivot_table(
                        Attendance,
                        values=[
                                'Girls Attended_S_Irreg',
                                'Boys Attended_S_Irreg',
                                'Total Attended_S_Irreg'],
                        index='Camp',
                        aggfunc='sum',
                        fill_value=0,
                        margins=True,
                        margins_name='Total')
                    st.dataframe(pivot_attend_s_ireg,use_container_width=True)


                st.write('## Attendance_check')
                with st.expander('Show the data'):
                    Attendance_check[['Girls_check', 'Boys_Check']] = Attendance_check[
                        ['Girls_check', 'Boys_Check']].fillna(0)
                    pivot_ac = pd.pivot_table(
                        Attendance_check,
                        values=[
                            'Girls_check',
                            'Boys_Check'],
                        index='Camp/Union',
                        aggfunc='sum',
                        fill_value=0,
                        margins=True,
                        margins_name='Total')
                    st.dataframe(pivot_ac, use_container_width=True)


                st.write("## Dropout")
                with st.expander("Show the data"):
                    # Print interventions associated with dropouts
                    Dropout = Dropout.rename(columns={'Camp/Union': 'Camp'})
                    # Replace NaN values with 0 in the dropout columns
                    Dropout[['Girls_Drop', 'Boys_Drop', 'Total_Drop']] = Dropout[
                        ['Girls_Drop', 'Boys_Drop', 'Total_Drop']].fillna(0)

                    # Convert to integer to ensure sum calculations work as expected
                    Dropout[['Girls_Drop', 'Boys_Drop', 'Total_Drop']] = Dropout[
                        ['Girls_Drop', 'Boys_Drop', 'Total_Drop']].astype(int)
                    # Display the pivot table
                    pivot_dropout = pd.pivot_table(
                        Dropout,
                        values=[
                            'Girls_Drop',
                            'Boys_Drop',
                            'Total_Drop'
                        ],
                        index='Camp',  # Only Camp in the index
                        aggfunc='sum',
                        fill_value=0,
                        margins=True,
                        margins_name='Total'
                    )
                    st.dataframe(pivot_dropout, use_container_width=True)
                    # Create the pivot table with both Camp and Intervention
                    pivot_dropout1 = pd.pivot_table(
                        Dropout,
                        values=[
                            'Girls_Drop',
                            'Boys_Drop',
                            'Total_Drop'
                        ],
                        index=['Camp', 'Intervention','Facility Name','Facility ID', 'Facility Type','Shift'],  # Include Intervention in the index
                        aggfunc='sum',
                        fill_value=0,
                        margins=True,
                        margins_name='Total'
                    )

                    # Filter pivot table to find interventions with dropouts
                    interventions_with_dropouts = pivot_dropout1[pivot_dropout1['Total_Drop'] > 0].reset_index()
                    #'Facility Name', 'Facility ID', 'Facility Type','Shift'
                    st.write("#### Interventions Associated with Dropouts")
                    st.dataframe(interventions_with_dropouts[['Camp', 'Facility Name','Intervention', 'Facility ID', 'Facility Type','Shift','Total_Drop']],use_container_width=True)


                st.write('## LF_Move')
                with st.expander('Show the data'):
                     pivot_LFmove1 = pd.pivot_table(
                         LF_move,
                         values=[
                               'Girls_Move_LF',
                               'Boys_Move_LF',
                               'Total_Move_LF'],
                         index='Camp/Union',
                         aggfunc='sum',
                         fill_value=0,
                         margins=True,
                         margins_name='Total')

                     st.dataframe(pivot_LFmove1,use_container_width=True)

                     pivot_LFmove2 = pd.pivot_table(
                         LF_move,
                         values=[
                             'Girls_Move_LF',
                             'Boys_Move_LF',
                             'Total_Move_LF'],
                         index=['Camp/Union','Intervention'],
                         aggfunc='sum',
                         fill_value=0,
                         margins=True,
                         margins_name='Total')
                     LF_move_associated = pivot_LFmove2[pivot_LFmove2['Total_Move_LF'] > 0].reset_index()
                     st.dataframe(LF_move_associated[['Camp/Union','Intervention','Total_Move_LF']],use_container_width=True)

                st.write('## Camp_Move')
                with st.expander('Show the data'):
                    pivot_Camp_move = pd.pivot_table(
                        Camp_move,
                        values=[
                            'Girls_Move_Camp',
                            'Boys_Move_Camp',
                            'Total_Move_Camp'],
                        index='Camp/Union',
                        aggfunc='sum',
                        fill_value=0,
                        margins=True,
                        margins_name='Total')

                    st.dataframe(pivot_Camp_move, use_container_width=True)

                st.write('## Phv')
                with st.expander('Show the data'):
                     pivot_phv = pd.pivot_table(
                        phv,
                        values=[
                            'Girls_PhV',
                            'Boys_PhV',
                            'Total_PhV'],
                        index='Camp/Union',
                        aggfunc='sum',
                        fill_value=0,
                        margins=True,
                        margins_name='Total')

                     st.dataframe(pivot_phv, use_container_width=True)


                st.write('## Facilitators')
                with st.expander('Show the data'):
                     Facilitators[['HC Female Teachers/ Facilitators',
                            'HC Male Teachers/ Facilitators',
                            'RC Female Rohingya Facilitators/ Teachers',
                            'RC Male Rohingya Facilitators/ Teachers']] =Facilitators[['HC Female Teachers/ Facilitators',
                            'HC Male Teachers/ Facilitators',
                            'RC Female Rohingya Facilitators/ Teachers',
                            'RC Male Rohingya Facilitators/ Teachers']].fillna(0)
                     Facilitators = Facilitators.rename(columns=
                         {'HC Female Teachers/ Facilitators':'HT_Female',
                          'HC Male Teachers/ Facilitators':'HT_Male',
                          'RC Female Rohingya Facilitators/ Teachers':'RT_Female',
                          'RC Male Rohingya Facilitators/ Teachers':'RT_Male'})
                     Facilitators['Total'] = Facilitators[['HT_Female','HT_Male','RT_Female','RT_Male']].sum(axis=1)

                     pivot_Facilitators = pd.pivot_table(
                        Facilitators,
                        values=[
                            'HT_Female',
                            'HT_Male',
                            'RT_Female',
                            'RT_Male',
                            'Total'],
                        index='Camp/Union',
                        aggfunc='sum',
                        fill_value=0,
                        margins=True,
                        margins_name='Total')

                     st.dataframe(pivot_Facilitators, use_container_width=True)

                st.write('## Volunteers')
                with st.expander('Show the data'):
                    pivot_Volunteers = pd.pivot_table(
                        Volunteers,
                        values=[
                            'HC Female Volunteers/ Guards',
                            'HC Male Volunteers/ Guards',
                            'RC Female Volunteers/ Guards',
                            'RC Male Volunteers/ Guards'],
                        index='Camp/Union',
                        aggfunc='sum',
                        fill_value=0,
                        margins=True,
                        margins_name='Total')
                    st.dataframe(pivot_Volunteers, use_container_width=True)

                    st.write('## CWD')
                    with st.expander('Show the data'):
                        pivot_cwd = pd.pivot_table(
                            cwd,
                            values=[
                                'Girls_CwD',
                                'Boys_CwD',
                                'Total_CwD'],
                            index='Camp/Union',
                            aggfunc='sum',
                            fill_value=0,
                            margins=True,
                            margins_name='Total')
                        st.dataframe(pivot_cwd, use_container_width=True)

            except Exception as e:
                st.error(f"Error reading file: {e}")

# Show login page or main app based on login status
if not st.session_state.logged_in:
    login()
else:
    app()
