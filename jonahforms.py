

import streamlit as st
import sqlite3
import pandas as pd
# import plotly.express as px
# import plotly.graph_objects as go
import time
# from streamlit_option_menu import option_menu

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

st.markdown(
    """
    <style>
    .main(
primaryColor : '#E84C29'
Background-color:'#273346'
font-color: '#FFFFFF'
font-family:"sans serif"
    )
    </style>
    """,
    unsafe_allow_html=True
)

# with open("style.css") as f:
#     st.markdown('<style>{f.read()}<style>', unsafe_allow_html=True)
conn = sqlite3.connect('data.db', check_same_thread=False)
cur = conn.cursor()
bigcollector = []
collector = []
entrysection = st.container()
mainsection = st.container()
loginsection = st.container()


facilityoptions = ["Select the Facility",
                   "Akamkpa General Hospital",
                   "Calabar General Hospital",
                   "Ugep General Hospital",
                   "Sankwala General Hospital",
                   "Initiative Of People Good Health (Ipgh) Youth Center",
                   "Calabar Municipal Youth Resource Center",
                   "Youth Hub Unical"]

LGAoptions = ["Select the LGA",
              "Calabar",
              "Akamkpa",
              "Yakurr",
              "Obanliku"
              ]
stateoptions = ["Select the State",
                "Cross river",
                "Akwa ibom",
                ]

Monthoptions = ["Select the Month",
                "January 2022",
                "February 2022",
                "March 2022",
                "April 2022",
                "May 2022",
                "June 2022",
                "July 2022",
                "August 2022",
                "September 2022",
                "October 2022",
                "November 2022",
                "December 2022"]

list = ["", "10-14yrs", "15-19yrs", "20-24yrs", "25-35yrs",
        "10-14yrs", "15-19yrs", "20-24yrs", "25-35yrs", ""]
listed = ["10-14yrs_male", "15-19yrs_male", "20-24yrs_male", "25-35yrs_male",
          "10-14yrs_female", "15-19yrs_female", "20-24yrs_female", "25-35yrs_female"]
# questions = ["Safe Sex", "STI Prevention", "Contraceptive Use",
#              "Drug Abuse", "Sexual Violence", "Unplanned Pregnancy", "Others (specify)"]

body = {
    "Total  Attendance":     ["Old Clients", "New Clients"],
    "Counseling on":            ["Safe Sex", "STI Prevention", "Contraceptive Use",
                                 "Drug Abuse", "Sexual Violence", "Unplanned Pregnancy", "Others (specify)"],
    " HIV Testing and Couseling": ["HIV Result negative (-ve)", "HIV Result positive (+ve)"],

    "Family Planning": ["Total no of clients receiving condom",
                        "Total no of condoms dispensed (in pieces)",
                        "Total no clients receiving Oral Contraceptive Pills (OPC)",
                        "Total no of clients receiving injectables",
                        "Total no of clients that had Implants inserted"],

    "HIV Care and Treatment": ["Enrolment into Care",
                               "HIV Treatment (ART)",
                               "PMTCT"],
    "Other Services": ["Post Abortion Care",
                       "Sydromic Management of STIs",
                       "Antenatal Care",
                       "Others"],
    "Treatment of Minor Ailments": ["Treatment of Minor Ailments"],
    "Group Contact Activities": ["Number of Adolescents and Young People reached through health talks held at the centre",
                                 "Number of School Visits Conducted",
                                 "Number of Adolescents and Young People reached through school visits",
                                 "Number of Outreaches /Group health talk conducted",
                                 "Number of Adolescents and Young People reached through outreaches/group health talks conducted"
                                 ],

    "Status": ["Number of  In School Youth (ISY) that accessed the centre",
               "Number of  Out School Youth (OSY) that accessed the centre",
               "Number of Clients referred",
               ]
}
keysList = [key for key in body]
# # print(keysList[1])
# questions = [body[i] for i in body]
# # print(questions[1][1])
if 'header' not in st.session_state:
    st.session_state['header'] = False


def authen(username, password):
    users = ['admin', 'CRSO', 'Bedet', 'Orose', 'Nchigbu',
             'Ionyekuru', 'Aapinega', 'Cthompson']
    passwods = ['admin', 'admin1', 'admin2', 'admin3',
                'admin4', 'admin5', 'admin6' 'admin7']

    col1, col2, col3 = st.columns(3)
    with col2:
        try:
            users.index(username) == passwods.index(password)

        except ValueError:
            st.session_state['loggedin'] = False
            st.error('Invalid Username or Password')

        else:
            st.session_state['loggedin'] = True
            if username == 'admin' and password == 'admin':
                st.session_state['header'] = True

            else:
                st.session_state['header'] = False


def showLogin():
    with loginsection:
        col1, col2, col3 = st.columns(3)

        with col2:
            st.write("## ASRH Monthly Data Collector")
            username = st.text_input("Enter your Username")
            password = st.text_input("Enter your Password", type="password")

            st.button("Login", on_click=authen, args=(username, password))


def spacer(order, number):
    for i in range(number):
        order.markdown(
            '<br/>', unsafe_allow_html=True)


def liner(order, number):
    for i in range(number):
        order.markdown(
            '<hr/>', unsafe_allow_html=True)


def spiller(title, questions):
    x = 0
    count = 0

    with st.expander(title):
        male, Female = st.columns(2)
        male.write(
            '<h4 class="small-font" style="text-align: center;">Male</h4>', unsafe_allow_html=True)
        Female.write(
            '<h4 class="small-font" style="text-align: center;">Female</h4>', unsafe_allow_html=True)
        cols = st.columns(10)
        count = 0

        for j in questions:

            for (i, col, e) in zip(list, cols, range(1, 11)):

                index = questions.index(j)+1

                e += index*10
                keys = j + str(e)
                if e == 1 or e % 10 == 1:

                    if (title in keysList[2:6] or title in keysList[0]):

                        col.markdown(
                            '<h6 class="small-font" style=" margin-top:25%;  ">{questions}</h6>'.format(questions=j), unsafe_allow_html=True)
                        spacer(col, 2)
                    elif (title == keysList[1]):
                        col.markdown(
                            '<h6 class="small-font" style=" margin-top:25%;  ">{questions}</h6>'.format(questions=j), unsafe_allow_html=True)

                        spacer(col, 3)
                    else:
                        col.markdown(
                            '<h6 class="small-font" style=" margin-top:26%;  ">{questions}</h6>'.format(questions=j), unsafe_allow_html=True)
                        # liner(col, 1)
                elif e % 10 == 0:

                    if questions.index(j) == count:
                        submitted1 = col.form_submit_button('sum', help=j)

                        if submitted1 == False:

                            col.write(
                                '<h5 class="vertical-center small-font" style="margin-left: 2.5%;">{fname}</h5>'.format(fname=0), unsafe_allow_html=True)
                        else:
                            hh = [sum(collector[i:i+len(questions)+1])
                                  for i in range(0, len(collector), len(questions)+1)]
                            col.write(
                                '<h5 class=" vertical-center small-font" style="margin-left: 2.5%;">{fname}</h5>'.format(fname=hh[questions.index(j)]), unsafe_allow_html=True)

                    else:
                        continue

                else:
                    x = col.number_input(i, min_value=0, key=keys)
                    collector.append(x)
                    liner(col, 1)
            liner(col, 1)
            count += 1


columns = []


def addData(holder):
    holder = []
    linelist = [body[i] for i in body]
    flat_list = [item for sublist in linelist for item in sublist]
    for y in listed:
        for x in flat_list:
            holder.append(x+y)

    header_columns_commands = []
    query = ""
    for h in holder:

        if h == holder[0]:

            header_columns_commands += "\"%s\"" % h.replace(" ", "_")
            header_columns_commands += " TEXT(4) "

        else:
            header_columns_commands += " , "
            header_columns_commands += "\"%s\"" % h.replace(" ", "_")
            header_columns_commands += " TEXT(4)"
    query += "CREATE TABLE IF NOT EXISTS ASRHMSF (\"Facility\" TEXT(50)  ,\"LGA\" TEXT(50)  ,\"State\" TEXT(50) ,\"Month\" TEXT(50)  , "
    query += "".join(header_columns_commands)
    query += ");"

    #########

    mark = []
    newquery = ""
    newcollector = [str(int(i)) for i in collector]
    bigcollector.extend(newcollector)
    for v in bigcollector[:4]:
        if v == bigcollector[0]:
            mark += "\"%s\"" % v
        else:
            mark += " , "
            mark += "\"%s\"" % v

    for v in bigcollector[4:]:
        if v == bigcollector[0]:
            mark += v

        else:
            mark += " , "
            mark += v

    newquery += "insert into ASRHMSF  values ( "
    newquery += "".join(mark)
    newquery += " );"
    try:

        cur.execute(query)
        cur.execute(newquery)
        # cur.execute(bad)

    except sqlite3.Error as error:
        st.write("Failed to insert data into sqlite table", error)
    finally:
        if conn:
            st.success("succesfully inserted")
            st.success("The SQLite connection is closed")
            conn.commit()
            conn.close()


def show_database():
    st.markdown("### ASRHMSF Monthly Reported data")

    cnx = sqlite3.connect('data.db')

    clean_df = pd.read_sql_query("SELECT * FROM ASRHMSF", cnx)

    st.dataframe(clean_df)


# def navbar():
#     selected = option_menu(
#         menu_title=None,
#         options=['Home', 'Database', 'Dashboard'],
#         icons=['house', 'wallet2', 'bar-chart'],
#         menu_icon="cast",
#         default_index=0,
#         orientation="horizontal",
#         styles={
#             "container": {"padding": "5!important", "background-color": "black", "width": "50%"},
#             "icon": {"color": "red", "font-size": "25px"},
#             "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "--hover-color": "#eee"},
#             "nav-link-selected": {"background-color": "#2C3845"},
#         }
#     )
#     if selected == "Home":
#         showmainpage()

#     elif selected == "Database":
#         show_database()

#     else:
#         show_dashboard()


def show_dashboard():
    st.write("Hello World")


def showmainpage():

    with mainsection:

        st.header("ASRH Monthly Data Collector")
        st.write(
            "Adolescents And Young People Reproductive Health Services Monthly Data Summary Form")
        liner(st, 1)

        with st.form(key='columns_in_form'):
            kol1, kol2, kol3, kol4 = st.columns(4)

            with kol1:
                facility = st.selectbox(
                    'Facility',
                    facilityoptions)
            with kol2:
                LGA = st.selectbox(
                    'LGA',
                    LGAoptions)
            with kol3:
                state = st.selectbox(
                    'State',
                    stateoptions)
            with kol4:
                month = st.selectbox(
                    'Reporting Month',
                    Monthoptions)

            liner(st, 1)
            spacer(st, 3)
            bigcollector.append(facility)
            bigcollector.append(LGA)
            bigcollector.append(state)
            bigcollector.append(month)
            st.markdown("### ASRH Monthly Summary Form (MSF)")
            spacer(st, 1)

            for key, value in body.items():
                spiller(key, value)

            submitted = st.form_submit_button('Submit')
            if submitted:
                addData(collector)


with entrysection:
    # st.title("ASRH Monthly Data Collector")
    if 'loggedin' not in st.session_state:
        st.session_state['loggedin'] = False
        showLogin()
    else:
        if st.session_state['loggedin']:
            with st.spinner("Loading..."):
                time.sleep(1)
                if st.session_state['header'] == True:
                    navbar()

        else:
            showLogin()
