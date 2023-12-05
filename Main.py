""" Project Title: Phonepe Pulse Data Visualization and Exporation: A User friendly Tool Using Streamlit and Plotly.
    Technologies Used: Github Cloning, Python, Pandas, MySQL, mysql-connector-python , Streamlit and Plotly
    Domain : FinTech
    Description: The Phonepe pulse Github repository contains a large amount of data related to various metrics and statistics. 
            The ETL.ipynb will extract this Github using cloning.
            and Main.py will process those extracted data to obtain insights and information that can be visualized in a user-friendly manner.    
"""



#---------------------------------------- / Libraries / ----------------------------------------


import streamlit as st
from PIL import Image
from streamlit_option_menu import option_menu
import mysql.connector
import pandas as pd
import plotly.express as px


#------------------------------------------ / Database Connection / --------------------------------

try:
    conn = mysql.connector.connect(
                            host = "localhost",
                            user = "root",
                            password = "mysql12345;",
                            database = "phonepe_data"
        )
    cursor = conn.cursor(buffered= True)
except mysql.connector.Error as err:
        print(f"Error: {err}")
    

#---------------------------------------- / Page Configuration / -----------------------------------------------------------------


icon = Image.open("ICN.png")
    
st.set_page_config(page_title= "Phonepe Pulse Data Visualization by Deepega",
                   page_icon= icon,
                   layout= "wide",
                   initial_sidebar_state= "expanded",
                   menu_items={'About': """# This dashboard app is created for PhonePe Data Visualization!
                                        Data has been cloned from Phonepe Pulse Github Repository"""})


#------------------------------------- / Menu option / -------------------------------------------------------------------


with st.sidebar:
    menu = option_menu("Menu", ["Home","Explore Data", "Top Charts","About"], 
                icons=["house","graph-up-arrow","bar-chart-line","circle"],
                menu_icon= "menu-button-wide",
                default_index=0,
                styles={"nav-link": {"font-size": "20px", "text-align": "left", "margin": "-2px", "--hover-color": "#6F36AD"},
                        "nav-link-selected": {"background-color": "#6F36AD"}})


#------------------------------------ / Home page / ----------------------------------------------------------------------

if menu == "Home":
    st.image("img.png")
    st.markdown("# :violet[Data Visualization and Exploration]")
    st.markdown("## :violet[A User-Friendly Tool Using Streamlit and Plotly]")
    col1,col2 = st.columns([3,2],gap="medium")
    with col1:
        st.write(" ")
        st.write(" ")
        st.markdown("### :violet[Domain :] Fintech")
        st.markdown("### :violet[Technologies used :] Github Cloning, Python, Pandas, MySQL, mysql-connector-python, Streamlit, and Plotly.")
        st.markdown("### :violet[Overview :] In this streamlit web app you can visualize the phonepe pulse data and gain lot of insights on transactions, number of users, top 10 state, district, pincode and which brand has most number of users and so on. Bar charts and Geo map visualization are used to get some insights.")
    with col2:
        st.image("home.png")


#------------------------------------ / Top charts Menu / ------------------------------------------------------------------------

if menu == "Top Charts":
    st.markdown("## :violet[Top Charts]")
    type = st.sidebar.selectbox(":violet[**Type**]", ("Transactions", "Users"))
    colum1,colum2= st.columns([1,1.5],gap="large")


    if type == "Transactions":
        with colum1:
            cursor.execute("SELECT DISTINCT Year from agg_trans")
            result = cursor.fetchall()
            years_list = [year[0] for year in result]
            year = st.selectbox(label= ":violet[**Year**]", options=years_list)
            quarter = st.selectbox(label=":violet[**Quarter**]", options = ["1", "2", "3", "4"])
            insights = st.selectbox(label= ":violet[**Insights**]", options=["State", "District", "Postal codes"])
        with colum2:
            st.info(
                    """
                    #### From this menu we can get insights like:
                    - Overall ranking on a particular Year and Quarter.
                    - Top 10 State, District, Pincode based on Total number of transaction and Total amount spent on PhonePe.
                    - Top 10 State, District, Pincode based on Total PhonePe users and their app opening frequency.
                    - Top 10 mobile brands and its percentage based on how many people use PhonePe.
                    """
                    )
    
        if insights == "State":
            st.markdown("### :violet[State - wise Transaction Data]")
            cursor.execute(f"select State, sum(Transaction_count) as Total_Transactions_Count, sum(Transaction_amount) as Total_Amount from agg_trans where Year = {year} and Quarter = {quarter} group by state order by Total_Amount desc limit 10")
            df = pd.DataFrame(cursor.fetchall(), columns=['State', 'Transactions_Count','Total_Amount'])
            if df.empty:
                st.info("##### :red[Sorry, Data Not available]")
            else:
                fig = px.bar(df, x='State', y='Total_Amount',
                title='Top 10 States by Total Amount',
                color='Transactions_Count',  
                color_continuous_scale=px.colors.sequential.Agsunset,  
                hover_data=['Transactions_Count'],
                labels={'Transactions_Count': 'Transactions Count'},
                text='Total_Amount',  
                )
                fig.update_layout(xaxis_title='State', yaxis_title='Total Amount')
                st.plotly_chart(fig,use_container_width=True)    


        if insights == "District":
            st.markdown("### :violet[District - wise Transaction Data]")
            cursor.execute(f"select District, sum(Number_of_transaction) as Total_Transaction_Count, sum(Amount) as Total_Amount from map_trans where Year = {year} and Quarter = {quarter} group by District order by Total_Amount desc limit 10")
            df = pd.DataFrame(cursor.fetchall(), columns=['District', 'Transaction_Count', 'Total_Amount'])
            if df.empty:
                st.info("##### :red[Sorry, Data Not available]")
            else:
                fig = px.bar(df,x='District', y='Total_Amount',
                            title= "Top 10 District by Total Amount",
                            color = "Transaction_Count",
                            color_continuous_scale=px.colors.sequential.Agsunset,  
                            hover_data=['Transaction_Count'],
                            labels={'Transactions_Count': 'Transactions Count'},
                            text='Total_Amount'
                            )
                fig.update_layout(xaxis_title='District', yaxis_title='Total Amount')
                st.plotly_chart(fig,use_container_width=True)


        if insights == "Postal codes":
            st.markdown("### :violet[Postal code - wise Transaction Data]")
            cursor.execute(f"select Pincode, sum(Transaction_count) as Total_Transaction_Count, sum(Transaction_amount) as Total_Amount from top_trans where Year= {year} and Quarter = {quarter} group by Pincode order by Total_Amount desc limit 10")
            df = pd.DataFrame(cursor.fetchall(), columns=['Pincode', 'Transaction_Count', 'Total_Amount'])
            df['Pincode'] = df['Pincode'].astype(str)
            if df.empty:
                st.info("##### :red[Sorry, Data Not available]")
            else:
                fig = px.bar(df, x= 'Pincode', y = 'Total_Amount',
                            title= "Top 10 Pincode by Total Amount",
                            color= "Transaction_Count",
                            color_continuous_scale= px.colors.sequential.Agsunset,
                            hover_data=['Transaction_Count'],
                            labels={'Transaction_Count' : 'Transaction Count'},
                            text= 'Total_Amount'
                            )
                fig.update_xaxes(type='category', categoryorder='array', categoryarray=df['Pincode'])
                fig.update_layout(xaxis_title = 'Postal Code', yaxis_title= 'Total Amount')
                st.plotly_chart(fig, use_container_width=True)

    if type == "Users":
        with colum1:
            cursor.execute("SELECT DISTINCT Year from agg_trans")
            result = cursor.fetchall()
            years_list = [year[0] for year in result]
            year = st.selectbox(label= ":violet[**Year**]", options=years_list)
            quarter = st.selectbox(label=":violet[**Quarter**]", options = ["1", "2", "3", "4"])
            insights = st.selectbox(label= ":violet[**Insights**]", options=["Brand", "District", "Postal codes"])


        with colum2:
            st.info(
                    """
                    #### From this menu we can get insights like:
                    - Overall ranking on a particular Year and Quarter.
                    - Top 10 State, District, Pincode based on Total number of transaction and Total amount spent on PhonePe.
                    - Top 10 State, District, Pincode based on Total PhonePe users and their app opening frequency.
                    - Top 10 mobile brands and its percentage based on how many people use PhonePe.
                    """
                    )
            

        if insights == "Brand":
            st.markdown("### :violet[Brand - wise User Data]")
            cursor.execute(f"Select Brand, sum(Count) as User_Count, sum(Percentage) as Percentage from agg_user where Year = {year} and Quarter = {quarter} group by Brand order by Percentage limit 10 ")
            df = pd.DataFrame(cursor.fetchall(),  columns = ["Brand", "Users_Count", "Percentage"])
            if df.empty:
                st.info("##### :red[Sorry, Data Not available]")
            else:
                fig = px.bar(df,
                                title=st.write(":violet[Top 10 Mobile brands]"),
                                x="Users_Count",
                                y="Brand",
                                orientation='h',
                                color='Percentage',
                                labels={"Users_Count" : "User Count"},
                                color_continuous_scale=px.colors.sequential.Agsunset)
                st.plotly_chart(fig,use_container_width=True)


        if insights == "District":
            st.markdown("### :violet[District - wise User Data]")
            cursor.execute(f"Select District_name, sum(Registered_User) as Total_users from map_user where Year = {year} and Quarter = {quarter} group by District_name order by Total_users desc limit 10")
            df = pd.DataFrame(cursor.fetchall(), columns=["District_name", "Total_users"])
            if df.empty:
                st.info("##### :red[Sorry, Data Not available]")
            else:
                fig = px.bar(df,
                             title= st.write(":violet[ Top 10 District have more Users]"),
                             x = "Total_users",
                             y = "District_name",
                             orientation='h',
                             color="Total_users",
                             labels= {"Total_users" : " User Count", "District_name" : "District"},
                             color_continuous_scale= px.colors.sequential.Agsunset)
                st.plotly_chart(fig, use_container_width= True)


        if insights == "Postal codes":
            st.markdown("### :violet[Postal code - wise User Data]")
            cursor.execute(f"select Pincode, sum(Registered_User) as Total_users from top_user where Year = {year} and Quarter = {quarter} group by Pincode order by Total_users desc limit 10")
            df = pd.DataFrame(cursor.fetchall(), columns=["Postal_code", "Total_users"])
            df["Postal_code"] = df['Postal_code'].astype(str)
            if df.empty:
                st.info("##### :red[Sorry, Data Not available]")
            else:
                fig = px.bar(df,
                             title=st.write(":violet[ Top 10 Postal areas have more Users]"),
                             x = "Total_users",
                             y = "Postal_code",
                             orientation='h',
                             color="Total_users",
                             labels= {"Total_users" : " User Count", "Postal_code" : "Postal Code"},
                             color_continuous_scale= px.colors.sequential.Agsunset)
                fig.update_yaxes(type='category', categoryorder='array', categoryarray=df['Postal_code'])
                st.plotly_chart(fig, use_container_width= True)


#-------------------------------------- / About Menu / --------------------------------------------------------------------

if menu == "About":
    st.image("phonepe_pulse.png")
    st.markdown("## :violet[About Phonepe pulse]")
    st.write("")
    st.write("")
    st.markdown("#### The Indian digital payments story has truly captured the world's imagination. From the largest towns to the remotest villages, there is a payments revolution being driven by the penetration of mobile phones and data.")
    st.write("")
    st.markdown("#### When PhonePe started 5 years back, we were constantly looking for definitive data sources on digital payments in India. Some of the questions we were seeking answers to were - How are consumers truly using digital payments? What are the top cases? Are kiranas across Tier 2 and 3 getting a facelift with the penetration of QR codes? This year as we became India's largest digital payments platform with 46% UPI market share, we decided to demystify the what, why and how of digital payments in India.")
    st.write("")
    st.markdown("#### This year, as we crossed 2000 Cr. transactions and 30 Crore registered users, we thought as India's largest digital payments platform with 46% UPI market share, we have a ring-side view of how India sends, spends, manages and grows its money. So it was time to demystify and share the what, why and how of digital payments in India.")
    st.write("")
    st.markdown("#### PhonePe Pulse is your window to the world of how India transacts with interesting trends, deep insights and in-depth analysis based on our data put together by the PhonePe team.")


#---------------------------------------- / Explore Data / -------------------------------------------------


if menu == "Explore Data":


    # ------------------------------------------ Date fetching for geo-visualization ------------------------------------


    districts = pd.read_csv('lat_long_district.csv')
    state = pd.read_csv('lat_long_state.csv')
    state = state.sort_values(by='state')
    state = state.reset_index(drop=True)
    state.rename(columns={'state': 'State'}, inplace= True)
    query1 = 'select * from agg_trans'
    df = pd.read_sql(query1, con=conn)
    query2 = 'select * from map_trans'
    districts_tran = pd.read_sql(query2, con=conn)

    query3 = 'select * from map_user'
    app_opening = pd.read_sql(query3, con=conn)
    query4 = 'select * from agg_user'
    user_device = pd.read_sql(query4, con=conn)
    df2 = df.groupby(['State']).sum()[['Transaction_count', 'Transaction_amount']]
    df2 = df2.reset_index()
    choropleth_data = state.copy()
    
    for column in df2.columns:
        if column != 'State':
        # If the column doesn't exist in choropleth_data, add it
            if column not in choropleth_data.columns:
                choropleth_data[column] = df2[column]


# ------------------------------------------ Date preparing for geo-visualization ------------------------------------


    df.rename(columns={'State': 'state'}, inplace=True)
    sta_list = ['andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh',
                    'assam', 'bihar', 'chandigarh', 'chhattisgarh',
                    'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat',
                    'haryana', 'himachal-pradesh', 'jammu-&-kashmir', 'jharkhand',
                    'karnataka', 'kerala', 'ladakh', 'lakshadweep', 'madhya-pradesh',
                    'maharashtra', 'manipur', 'meghalaya', 'mizoram', 'nagaland',
                    'odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim',
                    'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh',
                    'uttarakhand', 'west-bengal']
    state['state'] = pd.Series(data=sta_list)
    state_final = pd.merge(df, state, how='outer', on='state')
    districts_final = pd.merge(districts_tran, districts,
                                how='outer', on=['State', 'District'])

    # ------------------------------------------ plotting --------------------------------------------------------------------------------------


    with st.container():
        st.title(':violet[PhonePe Pulse Data Visualization(2018-2023)📈]')
        st.write(' ')
        st.subheader(
            ':violet[Registered user & App installed -> State and Districtwise:]')
        st.write(' ')
        scatter_year = st.selectbox('**:violet[Please select the Year]**',
                                    ('2018', '2019', '2020', '2021', '2022','2023'))
        st.write(' ')
        scatter_state = st.selectbox('**:violet[Please select State]**', ('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh',
                                                            'assam', 'bihar', 'chhattisgarh',
                                                            'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat',
                                                            'haryana', 'himachal-pradesh', 'jammu-&-kashmir', 'jharkhand',
                                                            'karnataka', 'kerala', 'ladakh', 'lakshadweep', 'madhya-pradesh',
                                                            'maharashtra', 'manipur', 'meghalaya', 'mizoram', 'nagaland',
                                                            'odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim',
                                                            'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh',
                                                            'uttarakhand', 'west-bengal'), index=25)
        scatter_year = int(scatter_year)
        scatter_reg_df = app_opening[(app_opening['Year'] == scatter_year) & (
            app_opening['State'] == scatter_state)]
        scatter_reg_df= scatter_reg_df.reset_index()
        scatter_register = px.scatter(scatter_reg_df, x="District", y="Registered_User",  color="District",
                                    hover_name="District", hover_data=['Year', 'Quarter','Registered_User'], size_max=100, opacity=0.8)
        
        st.plotly_chart(scatter_register)
        st.write(' ')


    # ------------------------------------- Streamlit Tabs for various analysis -----------------------------------------------------------------


    geo_analysis, Device_analysis, payment_analysis, transac_yearwise = st.tabs(
        ["Geographical analysis", "User device analysis", "Payment Types analysis", "Transacion analysis of States"])
    

    # ------------------------------------------- Geo-analysis ----------------------------------------------------------------------------------


    with geo_analysis:
        st.subheader(':violet[Transaction analysis->State and Districtwise:]')
        st.write(' ')
        Year = int(st.radio('Please select the Year',
                        ('2018', '2019', '2020', '2021', '2022','2023'), horizontal=True))
        st.write(' ')
        Quarter = int(st.radio('Please select the Quarter',
                        ('1', '2', '3', '4'), horizontal=True))
        st.write(' ')
        plot_district = districts_final[(districts_final['Year'] == Year) & (
            districts_final['Quarter'] == Quarter)]
        plot_state = state_final[(state_final['Year'] == Year)
                                & (state_final['Quarter'] == Quarter)]
        plot_state_total = plot_state.groupby(
            ['state', 'Year', 'Quarter', 'Latitude', 'Longitude']).sum()
        # plot_state_total = plot_state_total.drop_duplicates(subset=['State'])
        plot_state_total = plot_state_total.reset_index()

        state_code = ['AN', 'AD', 'AR', 'AS', 'BR', 'CH', 'CG', 'DNHDD', 'DL', 'GA',
                    'GJ', 'HR', 'HP', 'JK', 'JH', 'KA', 'KL', 'LA', 'LD', 'MP', 'MH',
                    'MN', 'ML', 'MZ', 'NL', 'OD', 'PY', 'PB', 'RJ', 'SK', 'TN', 'TS',
                    'TR', 'UP', 'UK', 'WB']
        plot_state_total['code'] = pd.Series(data=state_code)
        # st.dataframe(plot_district)
        fig1 = px.scatter_geo(plot_district,
                            lon=plot_district['Longitude'],
                            lat=plot_district['Latitude'],
                            color='Amount',
                            size=plot_district['Number_of_transaction'],
                            hover_name="District",
                            hover_data=["State", 'Amount',
                                        'Number_of_transaction', 'Year', 'Quarter'],
                            title='District',
                            size_max=22,)
        fig1.update_traces(marker=dict(color="#CC0044", line_width=1))
        fig1.update_traces(hovertemplate='<b>%{hovertext}<br><br>'
                                  '<b>State</b>: %{customdata[0]}<br>'
                                  '<b>Amount</b>: %{customdata[1]}<br>'
                                  '<b>Number_of_transaction</b>: %{customdata[2]}<br>'
                                  '<b>Year</b>: %{customdata[3]}<br>'
                                  '<b>Quarter</b>: %{customdata[4]}')

        fig2 = px.scatter_geo(plot_state_total,
                            lon=plot_state_total['Longitude'],
                            lat=plot_state_total['Latitude'],
                            hover_name='State',
                            text=plot_state_total['code'],
                            hover_data=['Transaction_count',
                                        'Transaction_amount', 'Year', 'Quarter'],
                            )
        fig2.update_traces(marker=dict(color="#D5FFCC", size=0.3))
        

        fig = px.choropleth(
            choropleth_data,
            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            featureidkey='properties.ST_NM',
            locations='State',
            color='Transaction_amount',
            color_continuous_scale='agsunset',
            hover_data=['Transaction_count', 'Transaction_amount']
        )

        fig.update_geos(fitbounds="locations", visible=False)
        fig.add_trace(fig1.data[0])
        fig.add_trace(fig2.data[0])
        fig.update_layout(height=1000, width=1000)
        st.write(' ')
        st.write(' ')
        if st.button('Click here to see map clearly'):
            fig.show(renderer="browser")
        st.plotly_chart(fig)


    # --------------------------------------------------- Device analysis statewise -------------------------------------------


    with Device_analysis:
        st.subheader(':violet[User Device analysis->Statewise:]')
        tree_map_state = st.selectbox('Please select State', ('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh',
                                                            'assam', 'bihar', 'chandigarh', 'chhattisgarh',
                                                            'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat',
                                                            'haryana', 'himachal-pradesh', 'jammu-&-kashmir', 'jharkhand',
                                                            'karnataka', 'kerala', 'ladakh', 'lakshadweep', 'madhya-pradesh',
                                                            'maharashtra', 'manipur', 'meghalaya', 'mizoram', 'nagaland',
                                                            'odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim',
                                                            'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh',
                                                            'uttarakhand', 'west-bengal'), index=10, key='tree_map_state')
        tree_map_state_year = int(st.radio('Please select the Year',
                                        ('2018', '2019', '2020', '2021', '2022', '2023'), horizontal=True, key='tree_map_state_year'))
        tree_map_state_quarter = int(st.radio('Please select the Quarter',
                                            ('1', '2', '3', '4'), horizontal=True, key='tree_map_state_quater'))
        user_device_treemap = user_device[(user_device['State'] == tree_map_state) & (user_device['Year'] == tree_map_state_year) &
                                        (user_device['Quarter'] == tree_map_state_quarter)]
        user_device_treemap['Count'] = user_device_treemap['Count'].astype(
            str)
        

        # ---------------------------------------- Barchart view of user device -----------------------------------------------------------------


        bar_user = px.bar(user_device_treemap, x='Brand', y='Count', color='Brand',
                        title='Bar chart analysis', color_continuous_scale='sunset',)
        st.plotly_chart(bar_user)


    # ----------------------------------------- Payment type analysis of Transacion data ----------------------------------------------------------


    with payment_analysis:
        st.subheader(':violet[Payment type Analysis -> 2018 - 2023:]')
        querypa = 'select * from agg_trans'
        payment_mode = pd.read_sql(querypa, con=conn)
        state = st.selectbox('Please select State', ('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh',
                                                                'assam', 'bihar', 'chandigarh', 'chhattisgarh',
                                                                'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat',
                                                                'haryana', 'himachal-pradesh', 'jammu-&-kashmir', 'jharkhand',
                                                                'karnataka', 'kerala', 'ladakh', 'lakshadweep', 'madhya-pradesh',
                                                                'maharashtra', 'manipur', 'meghalaya', 'mizoram', 'nagaland',
                                                                'odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim',
                                                                'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh',
                                                                'uttarakhand', 'west-bengal'), index=10, key='pie_pay_mode_state')
        year = int(st.radio('Please select the Year',
                                        ('2018', '2019', '2020', '2021', '2022','2023'), horizontal=True, key='pie_pay_year'))
        quarter = int(st.radio('Please select the Quarter',
                                            ('1', '2', '3', '4'), horizontal=True, key='pie_pay_quater'))
        values = st.selectbox(
            'Please select the values to visualize', ('Transaction_count', 'Transaction_amount'))
        payment_mode = payment_mode[(payment_mode['Year'] == year) & (
            payment_mode['Quarter'] == quarter) & (payment_mode['State'] == state)]
        

        # ------------------------------------- Bar chart analysis of payment mode ----------------------------------------------------------------


        bar_chart = px.bar(payment_mode, x='Transaction_type',
                        y=values, color='Transaction_type')
        st.plotly_chart(bar_chart)


        # --------------------------------------- Transacion data analysis statewise ------------------------------------------------------------------


    with transac_yearwise:
        st.subheader(':violet[Transaction analysis->Statewise:]')
        transac_state = st.selectbox('Please select State', ('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh',
                                                            'assam', 'bihar', 'chandigarh', 'chhattisgarh',
                                                            'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat',
                                                            'haryana', 'himachal-pradesh', 'jammu-&-kashmir', 'jharkhand',
                                                            'karnataka', 'kerala', 'ladakh', 'lakshadweep', 'madhya-pradesh',
                                                            'maharashtra', 'manipur', 'meghalaya', 'mizoram', 'nagaland',
                                                            'odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim',
                                                            'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh',
                                                            'uttarakhand', 'west-bengal'), index=10, key='transac')
        transac__quater = int(st.radio('Please select the Quarter',
                                    ('1', '2', '3', '4'), horizontal=True, key='trans_quater'))
        transac_type = st.selectbox('Please select the Mode',
                                    ('Recharge & bill payments', 'Peer-to-peer payments', 'Merchant payments', 'Financial Services', 'Others'), key='transactype')
        transac_values = st.selectbox(
            'Please select the values to visualize', ('Transaction_count', 'Transaction_amount'), key='transacvalues')

        new_df = df.groupby(
            ['state', 'Year', 'Quarter', 'Transaction_type']).sum()
        new_df = new_df.reset_index()
        chart = new_df[(new_df['state'] == transac_state) &
                    (new_df['Transaction_type'] == transac_type) & (new_df['Quarter'] == transac__quater)]
        

        # ------------------------------- Bar chart analysis of transacion data statewise --------------------------------------------------------


        year_fig = px.bar(chart, x=['Year'], y=transac_values, color=transac_values, color_continuous_scale='armyrose',
                        title='Transaction analysis '+transac_state + ' regarding to '+transac_type)
        st.plotly_chart(year_fig)



#------------------------------------ ****END OF CODE****----------------------------------------