import yaml
import json
import requests
import datetime
import streamlit as st 
import streamlit_authenticator as stauth

st.set_page_config(page_title="Ami Coding Parina")
st.sidebar.subheader("Ami Coding Parina")

def main():
    menu = ["Login","Signup"]
    choice = st.sidebar.selectbox('Menu',menu)
    time_stamp=""
    user_id=""
    payload=[]
    input_values=""
    inputs={
            "user_id":"", # Since we are using streamlit_authenticator and there are no user_id options, we are going with username as an API response for user_id
            "payload":payload
    }

    with open('./config.yaml') as file: # this config.yaml file is responsible for storing authentication credentials
        config = yaml.load(file,Loader=yaml.SafeLoader)

        authenticator = stauth.Authenticate(
            config['credentials'],
            config['cookie']['name'],
            config['cookie']['key'],
            config['cookie']['expiry_days'],
            config['preauthorized']
        )

    # #------------------------- Section 1 Login--------------------------

    if choice == "Login":
        
        name, authentication_status, username = authenticator.login('Login', 'main')

        if authentication_status:
            st.title("Khoj the Search",anchor="middle")
            st.write(f'Welcome ```{username}```')

            #------------------------- Section 2--------------------------
            st.header('Section 2:')
            st.markdown('___')

            csv=st.text_input('Input Values:')
            if csv:
                time_stamp=str(datetime.datetime.now())+","
                input_values=csv
                num_list=[int(i) for i in csv.split(',')]
                st.write(num_list)
            
            search_num=st.text_input('Search Value: ')
            
            if st.button("Khoj"):
                if int(search_num) in num_list:
                    st.subheader('Search Result: `True`')
                    st.subheader(f'At index:\t`{num_list.index(int(search_num))}`')
                else:
                    st.subheader('Search Result: `False`')
            
            #------------------------- Section 3--------------------------
            st.header("Section 3: ")
            st.markdown('___')
            url=st.text_input("Enter API URL:")
            st.markdown("You could press 'Post' Button to see the request body.")
            if st.button("Post"):
                time_stamp+=str(datetime.datetime.now())
                inputs["user_id"]=username
                payload.append({"time_stamp":time_stamp,"input_values":input_values})
                if url:
                    try:
                        res= requests.post(url=url,data=json.dumps(inputs))
                        st.write(f"Response: {res.text}")
                    except:
                        st.error("Please Enter correct URL")
                else:
                    st.write(inputs)


            authenticator.logout('Logout', 'sidebar')

        elif authentication_status == False:
            st.error('Username/password is incorrect')
        elif authentication_status == None:
            st.warning('Please enter your Username and Password')


# #------------------------- Section 1 Registration--------------------------

    elif choice == "Signup":
        try:
            if authenticator.register_user('Sign Up', preauthorization=False):
                with open('./config.yaml', 'w') as file:
                    yaml.dump(config, file, default_flow_style=False)
                st.success('User registered successfully')
        except Exception as e:
            st.error(e)


if __name__=='__main__':
    main()







    



