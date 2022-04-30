import streamlit as st
import sqlite3
import pandas as pd


st.set_page_config(layout="wide")
conn = sqlite3.connect('data.db', check_same_thread=False)
cur = conn.cursor()

entrysection = st.container()
mainsection = st.container()
loginsection = st.container()
collector = []
facilityoptions = ["SelecttheFacility",
                   "Akamkpa General Hospital",
                   "Calabar General Hospital",
                   "Ugep General Hospital",
                   "Sankwala General Hospital",
                   "Initiative Of People Good Health (Ipgh) Youth Center",
                   "Calabar Municipal Youth Resource Center",
                   "Youth Hub Unical"]

LGAoptions = ["SelecttheLGA",
              "Calabar",
              "Akamkpa",
              "Yakurr",
              "Obanliku"
              ]
stateoptions = ["SelecttheState",
                "Cross river",
                "Akwa ibom",
                ]

Monthoptions = ["SelecttheMonth",
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
# keysList = [key for key in body]
# # print(keysList[1])
# questions = [body[i] for i in body]
# # print(questions[1][1])


def authen(username, password):
    col1, col2, col3 = st.columns(3)
    with col2:
        if username == "admin" and password == "admin":
            st.session_state['loggedin'] = True
        else:
            st.session_state['loggedin'] = False
            st.error('Invalid Username or Password')


def showLogin():
    with loginsection:
        col1, col2, col3 = st.columns(3)

        with col2:
            st.write("## ASRH Monthly Data Collector")
            username = st.text_input("Enter your Username")
            password = st.text_input("Enter your Password", type="password")
            st.button("Login", on_click=authen, args=(username, password))


def spacer(number):
    for i in range(number):
        st.markdown(
            '<br/>', unsafe_allow_html=True)


def liner(number):
    for i in range(number):
        st.markdown(
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
                    if len(j) < 20:
                        col.markdown(
                            '<br/>', unsafe_allow_html=True)
                        col.markdown(
                            '<h6 class="small-font style="margin-top: 25%;">{questions}</h6>'.format(questions=j), unsafe_allow_html=True)
                        col.markdown(
                            '<hr/>', unsafe_allow_html=True)

                    else:
                        col.markdown(
                            '<h6 class="small-font">{questions}</h6>'.format(questions=j), unsafe_allow_html=True)

                elif e % 10 == 0:

                    if questions.index(j) == count:
                        submitted1 = col.form_submit_button('sum', help=j)

                        if submitted1 == False:

                            col.write(
                                '<h5 class="small-font" style="margin-left: 2.5%;">{fname}</h5>'.format(fname=0), unsafe_allow_html=True)
                        else:
                            hh = [sum(collector[i:i+len(questions)+1])
                                  for i in range(0, len(collector), len(questions)+1)]
                            col.write(
                                '<h5 class="small-font" style="margin-left: 2.5%;">{fname}</h5>'.format(fname=hh[questions.index(j)]), unsafe_allow_html=True)

                    else:
                        continue

                else:
                    x = col.number_input(i, min_value=0, key=keys)
                    collector.append(str(int(x)))
                    col.markdown(
                        '<hr/>', unsafe_allow_html=True)
            col.markdown(
                '<hr/>', unsafe_allow_html=True)

            count += 1


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

    for v in collector[:4]:
        if v == collector[0]:
            mark += "\"%s\"" % v
        else:
            mark += " , "
            mark += "\"%s\"" % v

    for v in collector[4:]:
        if v == collector[0]:
            mark += v

        else:
            mark += " , "
            mark += v
            # header_columns_commands += "\"%s\"" % h
    newquery += "insert into ASRHMSF  values ( "
    newquery += "".join(mark)
    newquery += " );"
    st.write(newquery)
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


def retrieve():

    try:
        cur.execute("Select * from ASRHMSF")
        data = cur.fetchall
        return data
    # cur.execute(bad)

    except sqlite3.Error as error:
        st.write("Failed to retrive data into sqlite table", error)
    finally:
        if conn:
            st.success("succesfully inserted")
            st.success("The SQLite connection is closed")


def showmainpage():

    with mainsection:
        st.header("ASRH Monthly Data Collector")
        st.write(
            "Adolescents And Young People Reproductive Health Services Monthly Data Summary Form")
        liner(1)

        with st.form(key='columns_in_form'):
            kol1, kol2, kol3, kol4 = st.columns(4)
            kole1, kole2, kole3, kole4 = st.columns(4)
            with kole2:
                getter = st.form_submit_button('retrieve')

                if getter:
                    st.write(collector)
                    result = retrieve()
                    clean_df = pd.DataFrame(result, columns=[collector])
                    st.dataframe(clean_df)

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

            liner(1)
            spacer(3)
            collector.append(facility)
            collector.append(LGA)
            collector.append(state)
            collector.append(month)
            st.markdown("### ASRH Monthly Summary Form (MSF)")
            spacer(1)

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
            showmainpage()
        else:
            showLogin()
