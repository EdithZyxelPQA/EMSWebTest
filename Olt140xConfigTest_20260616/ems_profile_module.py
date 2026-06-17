import time
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import selenium_module as mod
import web_share.EMS.ems_module as e_mod

from selenium.webdriver.common.keys import Keys
# .clear() -> .send_keys(Keys.CONTROL + 'a')

def Checkbox_EMS(driver,ele_id,request,index=''): # for ems check box
    index = str(index)
    check_box = driver.find_element(By.XPATH,f'//*[@for="{ele_id}{index}"]')
    if(driver.find_element(By.XPATH,f'//*[@id="{ele_id}{index}"]').is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()    

# User Continue ??? (copy from FW Web XPON Test)
def UserContinue(driver,username,password):
    try:
        driver.switch_to.default_content()
        driver.find_element(By.ID,"userContinue").click()
        driver.switch_to.frame(0)
    except:
        try:
            driver.switch_to.default_content()
            driver.find_element(By.CLASS_NAME, "ui-dialog.ui-widget.ui-widget-content.ui-corner-all.ui-front.ui-draggable")
            driver.find_element(By.ID,"lg_user").send_keys(username)
            driver.find_element(By.ID,"lg_pass").send_keys(password)
            driver.find_element(By.ID,"userLogin").click()
            driver.switch_to.frame(0)
        except:
            driver.switch_to.frame(0)

def Scroll(driver,id='profile_content_div',direction='Top',move=200,symbol='+'):
    element = driver.find_element('id',id)
    move = str(move)
    if(direction == 'Left'):
        symbol = '-'
    driver.execute_script(f'arguments[0].scroll{direction} = arguments[0].scroll{direction} {symbol} {move};',element)

def alert_accept(driver,timeout=10):
    return e_mod.alert_accept(driver,timeout)

def Wait_Block(driver):
    e_mod.Wait_Block(driver)

def get_ems_alert_msg(driver):
    return e_mod.get_ems_alert_msg(driver)
    
def alert_accept_text(driver, timeout=10):  # 60
    return e_mod.alert_accept_text(driver,timeout)

def if_msg_not_success(msg):
    return e_mod.if_msg_not_success(msg)
    
def If_Profile_Table_Full(driver,outp_id,profile_type,file_name,timeout1=10): 

    # full will print and return True

    total_data = driver.find_element(By.ID,'table_total_data_profile_table').text    
    if(('3000' in total_data) or ('2999' in total_data)):       

        print(f"             [Profile - {profile_type}] profile table full (3000 or 2999)  Delete 'Auto_max_...'...",file = open(file_name, '+a'))

        # Delete 'Auto_max'
        for i in range(2):
            if_find = False
            quantity_now = driver.find_elements(By.CLASS_NAME,"ProfileName").__len__()
            for index in range(quantity_now):
                if('Auto_max_' in driver.find_elements(By.CLASS_NAME,"ProfileName")[index].text):    
                    delete_target = driver.find_elements(By.CLASS_NAME,"ProfileName")[index].text
                    print(delete_target)            
                    Profile_Table_List_Checkbox(driver,index)               
                    Delete_Profile(driver)
                    msg = alert_accept_text(driver,timeout1)
                    if(if_msg_not_success(msg)):
                        print(f"             [Profile - {profile_type}] msg:{msg} {delete_target} Alert Delete Fail",file = open(file_name, '+a'))
                        if_temp_error = True
                        continue
                    else:
                        print(f"             [Profile - {profile_type}] msg:{msg} {delete_target} Alert Delete Pass",file = open(file_name, '+a'))
                    driver.find_element(By.LINK_TEXT,"Provision").click()
                    time.sleep(1)
                    driver.find_element(By.LINK_TEXT,"Profile").click()
                    time.sleep(1)
                    Profile_Select(driver, profile_type)
                    time.sleep(1)
                    # check profile name should not show in table            
                    if(Profile_Name_Search_only(driver,delete_target) == True):
                        print(f"             [Profile - {profile_type}] found {delete_target} after delete Delete Fail",file = open(file_name, '+a'))
                        if_temp_error = True
                    else:
                        print(f"             [Profile - {profile_type}] not found {delete_target} after delete Delete Pass",file = open(file_name, '+a'))
                    if_find = True
                    break
            if(if_find == False):
                print(f"             [Profile - {profile_type}] not found 'Auto_max_...' at first page before delete Delete Fail",file = open(file_name, '+a'))

        # try delete on other page
        Profile_Name_Sort_Click(driver)
        if(if_find == False):            
            time.sleep(2)
            for i in range(2):
                if_find2 = False
                quantity_now = driver.find_elements(By.CLASS_NAME,"ProfileName").__len__()
                for index in range(quantity_now):
                    if('Auto_max_' in driver.find_elements(By.CLASS_NAME,"ProfileName")[index].text):    
                        delete_target = driver.find_elements(By.CLASS_NAME,"ProfileName")[index].text
                        print(delete_target)            
                        Profile_Table_List_Checkbox(driver,index)               
                        Delete_Profile(driver)
                        msg = alert_accept_text(driver,timeout1)
                        if(if_msg_not_success(msg)):
                            print(f"             [Profile - {profile_type}] msg:{msg} {delete_target} Alert Delete Fail",file = open(file_name, '+a'))
                            if_temp_error = True
                            continue
                        else:
                            print(f"             [Profile - {profile_type}] msg:{msg} {delete_target} Alert Delete Pass",file = open(file_name, '+a'))
                        driver.find_element(By.LINK_TEXT,"Provision").click()
                        time.sleep(1)
                        driver.find_element(By.LINK_TEXT,"Profile").click()
                        time.sleep(1)
                        Profile_Select(driver, profile_type)
                        time.sleep(1)
                        # check profile name should not show in table            
                        if(Profile_Name_Search_only(driver,delete_target) == True):
                            print(f"             [Profile - {profile_type}] found {delete_target} after delete Delete Fail",file = open(file_name, '+a'))
                            if_temp_error = True
                        else:
                            print(f"             [Profile - {profile_type}] not found {delete_target} after delete Delete Pass",file = open(file_name, '+a'))
                        if_find2 = True
                        break
                if(if_find2 == False):
                    print(f"             [Profile - {profile_type}] not found 'Auto_max_...' at first page before delete Delete Fail",file = open(file_name, '+a'))

        # check again
        total_data = driver.find_element(By.ID,'table_total_data_profile_table').text    
        print(f"             [Profile - {profile_type}] profile table entries now {total_data}",file = open(file_name, '+a'))
        if(('3000' in total_data) or ('2999' in total_data)):    

            print(f"             [Profile - {profile_type}] profile table full (3000 or 2999)",file = open(file_name, '+a'))
            if(outp_id == '0'):
                print(f"             [Profile - {profile_type}] Result Fail",file = open(file_name, '+a'))
            else:
                print(f"  [{outp_id}][Profile - {profile_type}] Result Fail",file = open(file_name, '+a'))
                print("======================================================================================",file = open(file_name, '+a'))
            return True
    else:
        print(f"",file = open(file_name, '+a'))
        return False

# Click 'OK', it will show 'value format error while use .clear() on text input'
def Click_OK_format_error(driver):
    try:
        driver.find_element(By.XPATH,'//*[@id="message_diag"]/div/div/div[3]/button').click()      # OK
    except:
        pass    

def Clear_Input_text(driver,ele):
    # fire keyboard event to clear text (Ctrl + Backspace)
    driver.find_element('css_selector',ele).send_keys(u'\ue009' + u'\ue003')

# Profile     (suit ALL)

def Profile_Select(driver,text):
    Select(driver.find_element(By.ID,"profile_filtertype")).select_by_visible_text(text)
    time.sleep(0.5)

def New_Profile(driver):
    driver.find_element(By.ID,"i_action_create_collector").click()
    # driver.find_element(By.XPATH,'//*[@title="New Profile"]').click()
    time.sleep(0.3)

def Delete_Profile(driver):
    driver.find_element(By.ID,"i_action_delete").click()
    # driver.find_element(By.XPATH,'//*[@title="Delete Profile"]').click()

def Save(driver):
    driver.find_element(By.XPATH,'//*[@value="Save"]').click()

def OK(driver):
    driver.find_element(By.ID,'popupCallBack').click()

def Close(driver):
    driver.find_element(By.ID,'popupClose').click()

def Refresh(driver):
    driver.find_element(By.ID,'i_action_refresh').click()

def Profile_Mode(driver):
    # Edit text
    return driver.find_element(By.XPATH,'//*[@id="edit_profile_background"]/div[1]/div').text
    # Create text
    # return driver.find_element(By.XPATH,'//*[@id="create_profile_background"]/div[1]/div').text
# //*[@id="create_profile_background"]/div[1]/div

def Profile_Name(driver,value):
    driver.find_element(By.ID,"profile_name").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"profile_name").send_keys(value)

def Profile_Path(driver,text):
    driver.switch_to.default_content()
    time.sleep(1) 
    driver.find_element(By.LINK_TEXT,"Provision").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT,"Profile").click()
    time.sleep(1)

    Profile_Select(driver,text)
    time.sleep(1)

def Edit(driver,index):
    driver.find_elements(By.NAME,"tdModify")[index].click()

def Profile_Name_Sort_Click(driver):
    # sort profile name (click)
    driver.find_element(By.XPATH,'//*[@name="Name" and @class="dragaccept"]').click()

def Profile_Table_List_Checkbox(driver,index):
    driver.find_element(By.XPATH,f"//*[@for='myCheckbox{index}_profile_table']").click()

def Profile_Table_List_Edit_Name(driver,name):

    # Search + click Edit
    # (only the first and the last page)
        
    for i in range(2):
        # sort profile name (click)
        Profile_Name_Sort_Click(driver)
        # quick check if profile in this page    
        if(Profile_Name_Search_only(driver,name) == True):      
            # search     
            quantity_now = driver.find_elements(By.CLASS_NAME,"ProfileName").__len__()
            for index in range(quantity_now):
                if(driver.find_elements(By.CLASS_NAME,"ProfileName")[index].text == name):                
                    Edit(driver,index)
                    time.sleep(3)
                    return True
                    break
        
    # profile name may exist in middle page, but wont keep search
    time.sleep(3)
    return False


def Profile_Name_Search(driver,name): 
    # only serch the first and the last page, middle page wont search   # return index

    for i in range(2):
        # sort profile name (click)
        Profile_Name_Sort_Click(driver)        
        # quick check if profile in this page
        if(Profile_Name_Search_only(driver,name) == True): 
            # search
            quantity_now = driver.find_elements(By.CLASS_NAME,"ProfileName").__len__()
            for index in range(quantity_now):
                if(driver.find_elements(By.CLASS_NAME,"ProfileName")[index].text == name):                
                    Edit(driver,index)
                    return index
                    break

    # if not found
    return -1 

def Profile_Name_Search_only(driver,name):
    # only search , wont return index

    # faster search check if text on HTML

    try:
        # driver.find_elements(By.XPATH, "//*[contains(text(), 'Auto_max_1072')]")  # V
        # driver.find_element(By.XPATH,f'//*[@val="{name}" and @class="ProfileName"]')  # V
        timeout = 3
        WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH,f'//*[@val="{name}" and @class="ProfileName"]'))) #.click()
        return True
    except:
        return False

# def Profile_Table_List_Checkbox_Name(driver,name):
#     # sort profile name (click)
#     driver.find_element(By.XPATH,'//*[@name="Name" and @class="dragaccept"]').click()
#     # search
#     quantity_now = driver.find_elements(By.CLASS_NAME,"ProfileName").__len__()
#     for index in range(quantity_now):
#         if(driver.find_elements(By.CLASS_NAME,"ProfileName")[index].text == name):                
#             Profile_Table_List_Checkbox(driver,index)
#             return True
#             break
#     # sort profile name (click)
#     driver.find_element(By.XPATH,'//*[@name="Name" and @class="dragaccept"]').click()
#     # search    
#     quantity_now = driver.find_elements(By.CLASS_NAME,"ProfileName").__len__()
#     for index in range(quantity_now):
#         if(driver.find_elements(By.CLASS_NAME,"ProfileName")[index].text == name):                
#             Profile_Table_List_Checkbox(driver,index)
#             return True
#             break
#     # profile name may exist in middle page, but wont keep search
#     return False


# Template Profile

def Template_New(driver):
    New_Profile(driver)

def Template_Delete(driver):
    # driver.find_element(By.NAME, "rpXgponTemplate_TablebtnDelete").click()
    Delete_Profile(driver)

# def Template_Delete_All_Select(driver,request):
#     check_box = driver.find_element(By.NAME, "rpXGSponTemplate_chkDelall")
#     if(check_box.is_selected() == True):
#         if(request == False):
#             check_box.click()
#     else:
#         if(request == True):
#             check_box.click()
# ###
# # def Template_Delete_Select_1(driver):
# #     check_box = driver.find_elements(By.NAME, "rpXGSponTemplate_chkDel")[0].click()

# # def Template_Delete_Select_2(driver):
# #     check_box = driver.find_elements(By.NAME, "rpXGSponTemplate_chkDel")[1].click()

# def Template_Delete_Select(driver,index):
#     driver.find_elements(By.NAME, "rpXGSponTemplate_chkDel")[index-1].click()

def Template_New_Name(driver,value):
    # driver.find_element(By.ID, "rpXGSponTemplate_IptProfName").clear()
    # driver.find_element(By.ID, "rpXGSponTemplate_IptProfName").send_keys(value)
    Profile_Name(driver,value)

def Template_New_Apply(driver):
    Save(driver)

# def Template_New_Delete(driver):
#     driver.find_elements(By.CLASS_NAME, "ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-text-only")[1].click()

# def Template_New_fec(driver,request):
#     check_box = driver.find_element(By.ID, f"rpXGSponTemplate_Fec")
#     if(check_box.is_selected() == True):
#         if(request == False):
#             check_box.click()
#     else:
#         if(request == True):
#             check_box.click()

# # ###
# def Template_New_UNI_Profile(driver,text):
#     Select(driver.find_element(By.ID, "rpXGSponTemplate_UniProf")).select_by_visible_text(text)

# def Template_New_Security_Profile(driver,text):
#     Select(driver.find_element(By.ID, "rpXGSponTemplate_SecuProf")).select_by_visible_text(text)

# def Template_New_Alarm_Profile(driver,text):
#     Select(driver.find_element(By.ID, "rpXGSponTemplate_AlarmProf")).select_by_visible_text(text)

# def Template_New_Ont_Profile(driver,text):
#     Select(driver.find_element(By.ID, "rpXGSponTemplate_OntProf")).select_by_visible_text(text)
###
# Template Profile - Main

def Template_New_Main_UNI_Profile(driver,text):
    Select(driver.find_element(By.ID,f"ont_template_uni_profile_combobox")).select_by_visible_text(text)

def Template_New_Main_Security_Profile(driver,text):
    Select(driver.find_element(By.ID,f"ont_template_security_profile_combobox")).select_by_visible_text(text)

def Template_New_Main_Alarm_Profile(driver,text):
    Select(driver.find_element(By.ID,f"ont_template_alarm_profile_combobox")).select_by_visible_text(text)

def Template_New_Main_Ont_Profile(driver,text):
    Select(driver.find_element(By.ID,f"ont_template_ONT_profile_combobox")).select_by_visible_text(text)

def Template_New_Main_DS_PIR(driver,text):
    driver.find_element(By.ID,"ont_template_ds_pir_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"ont_template_ds_pir_text").send_keys(text)

# Template Profile -> Service

def Template_New_Service_Profile_Active_all(driver,request):
    # check_box = driver.find_element(By.XPATH,'//*[@for="ont_template_service_enable_checkboxall"]')
    # if(check_box.is_selected() == True):
    #     if(request == False):
    #         check_box.click()
    # else:
    #     if(request == True):
    #         check_box.click()
    Checkbox_EMS(driver,f'ont_template_service_enable_checkboxall',request)

def Template_New_Service_Profile_Active_Select(driver,index,request):
    # check_box = driver.find_element(By.XPATH,f'//*[@for="ont_template_service_enable_checkbox{index}"]')
    # if(check_box.is_selected() == True):
    #     if(request == False):
    #         check_box.click()
    # else:
    #     if(request == True):
    #         check_box.click()
    Checkbox_EMS(driver,f'ont_template_service_enable_checkbox{index}',request)

def Template_New_Service_Profile_all(driver,text):
    Select(driver.find_element(By.ID,"ont_template_service_comboboxall")).select_by_visible_text(text)
    # Select(driver.find_element(By.NAME,"rpXGSponTemplate_slt_saServiceProf")).select_by_visible_text(text)
    # unable use on website, it is in <!-- -->
def Template_New_Service_Profile_Select(driver,index,text):
    Select(driver.find_element(By.ID,f"ont_template_service_combobox{index}")).select_by_visible_text(text)

def Template_New_Service_Shared_Priority_all(driver,text):
    Select(driver.find_element(By.ID,"ont_template_service_shared_comboboxall")).select_by_visible_text(text)

def Template_New_Service_Shared_Priority_Select(driver,index,text):
    Select(driver.find_element(By.ID,f"ont_template_service_shared_combobox{index}")).select_by_visible_text(text)

def Template_New_Service_US_Bandwidth_Profile_all(driver,text):
    Select(driver.find_element(By.ID,"ont_template_service_us_bw_comboboxall")).select_by_visible_text(text)

def Template_New_Service_US_Bandwidth_Profile_Select(driver,index,text):
    Select(driver.find_element(By.ID,f"ont_template_service_us_bw_combobox{index}")).select_by_visible_text(text)

def Template_New_Service_DS_Bandwidth_Profile_all(driver,text):
    Select(driver.find_element(By.ID,"ont_template_service_ds_bw_comboboxall")).select_by_visible_text(text)

def Template_New_Service_DS_Bandwidth_Profile_Select(driver,index,text):
    Select(driver.find_element(By.ID,f"ont_template_service_ds_bw_combobox{index}")).select_by_visible_text(text)


# Template Profile -> T-cont

def Template_New_Tcont_Service_List_Active_all(driver,request):
    # check_box = driver.find_element(By.XPATH,f'//*[@for="ont_template_tcont_enable_checkboxall"]')
    # if(check_box.is_selected() == True):
    #     if(request == False):
    #         check_box.click()
    # else:
    #     if(request == True):
    #         check_box.click()
    Checkbox_EMS(driver,f'ont_template_tcont_enable_checkboxall',request)

def Template_New_Tcont_Service_List_Active_Select(driver,index,request):
    # check_box = driver.find_element(By.XPATH,f'//*[@for="ont_template_tcont_enable_checkbox{index}"]')
    # if(check_box.is_selected() == True):
    #     if(request == False):
    #         check_box.click()
    # else:
    #     if(request == True):
    #         check_box.click()
    Checkbox_EMS(driver,f'ont_template_tcont_enable_checkbox{index}',request)

def Template_New_Tcont_Service_List_all(driver,text):
    Select(driver.find_element(By.ID,"ont_template_tcont_comboboxall")).select_by_visible_text(text)

def Template_New_Tcont_Service_List_Select(driver,index,text):
    Select(driver.find_element(By.ID,f"ont_template_tcont_combobox{index}")).select_by_visible_text(text)

def Template_New_Tcont_US_Bandwidth_Profile_all(driver,text):
    Select(driver.find_element(By.ID,"ont_template_tcont_us_bw_comboboxall")).select_by_visible_text(text)

def Template_New_Tcont_US_Bandwidth_Profile_Select(driver,index,text):
    Select(driver.find_element(By.ID,f"ont_template_tcont_us_bw_combobox{index}")).select_by_visible_text(text)

def Template_New_Tcont_DS_Bandwidth_Profile_all(driver,text):
    Select(driver.find_element(By.ID,"ont_template_tcont_ds_bw_comboboxall")).select_by_visible_text(text)

def Template_New_Tcont_DS_Bandwidth_Profile_Select(driver,index,text):
    Select(driver.find_element(By.ID,f"ont_template_tcont_ds_bw_combobox{index}")).select_by_visible_text(text)

def Template_New_Tcont_Type_all(driver,text):
    Select(driver.find_element(By.ID,"ont_template_tcont_type_comboboxall")).select_by_visible_text(text)

def Template_New_Tcont_Type_Select(driver,index,text):
    Select(driver.find_element(By.ID,f"ont_template_tcont_type_combobox{index}")).select_by_visible_text(text)


# Template Profile -> Multicast

def Template_New_Multicast_Profile_Active_all(driver,request):
    # check_box = driver.find_element(By.XPATH,f'//*[@for="ont_template_multicast_enable_checkboxall"]')
    # if(check_box.is_selected() == True):
    #     if(request == False):
    #         check_box.click()
    # else:
    #     if(request == True):
    #         check_box.click()
    Checkbox_EMS(driver,f'ont_template_multicast_enable_checkboxall',request)

def Template_New_Multicast_Profile_Active_Select(driver,index,request):
    # check_box = driver.find_element(By.XPATH,f'//*[@for="ont_template_multicast_enable_checkbox{index}"]')
    # if(check_box.is_selected() == True):
    #     if(request == False):
    #         check_box.click()
    # else:
    #     if(request == True):
    #         check_box.click()
    Checkbox_EMS(driver,f'ont_template_multicast_enable_checkbox{index}',request)

def Template_New_Multicast_Profile_all(driver,text):
    Select(driver.find_element(By.ID,"ont_template_multicast_comboboxall")).select_by_visible_text(text)

def Template_New_Multicast_Profile_Select(driver,index,text):
    Select(driver.find_element(By.ID,f"ont_template_multicast_combobox{index}")).select_by_visible_text(text)


# # def Template_New_tcont_Active_all(driver,request):
# #     check_box = driver.find_element(By.NAME, "rpXGSponTemplate_saTcontActive")
# #     if(check_box.is_selected() == True):
# #         if(request == False):
# #             check_box.click()
# #     else:
# #         if(request == True):
# #             check_box.click()

# # def Template_New_US_Bandwidth_Profile_all(driver,text):
# #     Select(driver.find_element(By.NAME, "rpXGSponTemplate_slt_saTcontUSBWProf")).select_by_visible_text(text)

# # def Template_New_DS_Bandwidth_Profile_all(driver,text):
# #     Select(driver.find_element(By.NAME, "rpXGSponTemplate_slt_saTcontDSBWProf")).select_by_visible_text(text)

# # def Template_New_Multicast_Profile_Active_all(driver,request):
# #     check_box = driver.find_element(By.NAME, "rpXGSponTemplate_saMcastActive")
# #     if(check_box.is_selected() == True):
# #         if(request == False):
# #             check_box.click()
# #     else:
# #         if(request == True):
# #             check_box.click()

# # def Template_New_Multicast_Profile_all(driver,text):
# #     Select(driver.find_element(By.NAME, "rpXGSponTemplate_slt_saMcastProf")).select_by_visible_text(text)

# Service Profile   

def Service_Profile_New(driver):
    New_Profile(driver)

def Service_Profile_Delete(driver):
    Delete_Profile(driver)

# def Service_Profile_Delete_All_Select(driver,request):
#     check_box = driver.find_element(By.NAME, "rpXGSponSecuProf_chkDelall")
#     if(check_box.is_selected() == True):
#         if(request == False):
#             check_box.click()
#     else:
#         if(request == True):
#             check_box.click()

# def Service_Profile_Delete_Select(driver,index):
#     driver.find_elements(By.NAME, "rpXGSponServiceProf_chkDel")[index-1].click()

def Service_Profile_New_Name(driver,value):
    driver.find_element(By.ID,"profile_name").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"profile_name").send_keys(value)

def Service_Profile_New_VLAN(driver,value):
    driver.find_element(By.ID,"ont_service_vlan_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"ont_service_vlan_text").send_keys(value)

def Service_Profile_New_Mapper_Pbits(driver,num,request):
    # check_box = driver.find_element(By.XPATH,f"//*[@for='ont_service_pbit{num}_checkbox']")
    # if(check_box.is_selected() == True):
    #     if(request == False):
    #         check_box.click()
    # else:
    #     if(request == True):
    #         check_box.click()
    Checkbox_EMS(driver,f'ont_service_pbit{num}_checkbox',request)

def Service_Profile_New_Lan_mode_veip(driver):
    driver.find_element(By.XPATH,f"//*[@for='ont_service_veip_radio']").click()

def Service_Profile_New_Lan_mode_bridge(driver):
    driver.find_element(By.XPATH,f"//*[@for='ont_service_bridge_radio']").click()

def Service_Profile_New_Lan(driver,val):
    # Select(driver.find_element(By.ID,"ont_service_lan_combobox")).select_by_visible_text(text)
    Select(driver.find_element(By.ID,"ont_service_lan_combobox")).select_by_value(val)

# def Service_Profile_New_Vlan_xc(driver,value):
#     driver.find_element(By.ID, "rpXGSponServiceProf_vlanxc").clear()
#     driver.find_element(By.ID, "rpXGSponServiceProf_vlanxc").send_keys(value)

# def Service_Profile_New_Vlan_xc_mode_enable(driver):
#     driver.find_elements(By.ID, "rpXGSponServiceProf_vlanxcmode")[0].click()

# def Service_Profile_New_Vlan_xc_mode_disable(driver):
#     driver.find_elements(By.ID, "rpXGSponServiceProf_vlanxcmode")[1].click()

def Service_Profile_New_Apply(driver):
    Save(driver)

# def Service_Profile_New_Delete(driver):
#     driver.find_elements(By.CLASS_NAME, "ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-text-only")[1].click()

#     # try:
#     #     driver.find_element(By.ID, "rpXGSponServiceProf_vlanxcmode")
#     #     print("yes",file = open("Web_auto_Report.txt", '+a'))
#     # except:
#     #     print("no",file = open("Web_auto_Report.txt", '+a'))

# QoS Bandwidth Profile

def QoS_Bandwidth_Profile_New(driver):
    New_Profile(driver)

def QoS_Bandwidth_Profile_Delete(driver):
    Delete_Profile(driver)

# def QoS_Bandwidth_Profile_Delete_All_Select(driver,request):
#     check_box = driver.find_element(By.NAME, "rpXGSponQosBwProf_chkDelall")
#     if(check_box.is_selected() == True):
#         if(request == False):
#             check_box.click()
#     else:
#         if(request == True):
#             check_box.click()

def QoS_Bandwidth_Profile_New_Name(driver,value):
    Profile_Name(driver,value)

def QoS_Bandwidth_Profile_New_sir(driver,value):
    # driver.find_element(By.ID,"ont_bandwidth_sir_text").clear()
    driver.find_elements(By.ID,'ont_bandwidth_sir_text')[0].send_keys(Keys.CONTROL + 'a')  # fire keyboard
    driver.find_elements(By.ID,"ont_bandwidth_sir_text")[0].send_keys(value)

def QoS_Bandwidth_Profile_New_air(driver,value):
    # driver.find_element(By.ID,"ont_bandwidth_air_text").send_keys(Keys.CONTROL + 'a')
    driver.find_elements(By.ID,"ont_bandwidth_air_text")[0].send_keys(Keys.CONTROL + 'a')  # fire keyboard
    driver.find_elements(By.ID,"ont_bandwidth_air_text")[0].send_keys(value)

def QoS_Bandwidth_Profile_New_pir(driver,value):
    # driver.find_element(By.ID,"ont_bandwidth_pir_text").send_keys(Keys.CONTROL + 'a')
    driver.find_elements(By.ID,"ont_bandwidth_pir_text")[0].send_keys(Keys.CONTROL + 'a')  # fire keyboard
    driver.find_elements(By.ID,"ont_bandwidth_pir_text")[0].send_keys(value)

def QoS_Bandwidth_Profile_New_GPON_Fallback_Rate_SIR(driver,value):
    driver.find_elements(By.ID,'ont_bandwidth_sir_text')[1].send_keys(Keys.CONTROL + 'a')  
    driver.find_elements(By.ID,"ont_bandwidth_sir_text")[1].send_keys(value)

def QoS_Bandwidth_Profile_New_GPON_Fallback_Rate_AIR(driver,value):
    driver.find_elements(By.ID,'ont_bandwidth_air_text')[1].send_keys(Keys.CONTROL + 'a')  
    driver.find_elements(By.ID,"ont_bandwidth_air_text")[1].send_keys(value)

def QoS_Bandwidth_Profile_New_GPON_Fallback_Rate_PIR(driver,value):
    driver.find_elements(By.ID,'ont_bandwidth_pir_text')[1].send_keys(Keys.CONTROL + 'a')  
    driver.find_elements(By.ID,"ont_bandwidth_pir_text")[1].send_keys(value)

def QoS_Bandwidth_Profile_New_Apply(driver):
    Save(driver)

def QoS_Bandwidth_Profile_New_Delete(driver):
    Delete_Profile(driver)

# Multicast Profile

def Multicast_Profile_New(driver):
    New_Profile(driver)

def Multicast_Profile_Delete(driver):
    Delete_Profile(driver)

# def Multicast_Profile_Delete_All_Select(driver,request):
#     check_box = driver.find_element(By.NAME, "rpXGSponMcastProf_chkDelall")
#     if(check_box.is_selected() == True):
#         if(request == False):
#             check_box.click()
#     else:
#         if(request == True):
#             check_box.click()

# def Multicast_Profile_Delete_Select(driver,index):
#     driver.find_elements(By.NAME, "rpXGSponMcastProf_chkDel")[index-1].click()

def Multicast_Profile_New_Name(driver,value):
    Profile_Name(driver,value)

def Multicast_Profile_New_UNI_VID(driver,value):
    # driver.find_element(By.ID,"ont_multicast_vid_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"ont_multicast_vid_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"ont_multicast_vid_text").send_keys(value)
    
def Multicast_Profile_New_IGMP_Version(driver,text):
    Select(driver.find_element(By.ID,"ont_multicast_igmp_version_combobox")).select_by_visible_text(text)
    
def Multicast_Profile_New_Tx_Tag_Mode(driver,text):
    Select(driver.find_element(By.ID,"ont_multicast_txmode_combobox")).select_by_visible_text(text)

def Multicast_Profile_New_Tx_Tag_VID(driver,value):
    driver.find_element(By.ID,"ont_multicast_txmode_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"ont_multicast_txmode_text").send_keys(value)
    
def Multicast_Profile_New_Tx_Tag_Pbit(driver,text):
    Select(driver.find_element(By.ID,"ont_multicast_txpbit_combobox")).select_by_visible_text(text)
    
def Multicast_Profile_New_Group_Privilege_Profile(driver,text):
    Select(driver.find_element(By.ID,"ont_multicast_gpprofile_combobox")).select_by_visible_text(text)

def Multicast_Profile_New_Max_Group(driver,value):
    driver.find_element(By.ID,"ont_multicast_maxgroup_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"ont_multicast_maxgroup_text").send_keys(value)

def Multicast_Profile_New_Max_Message(driver,value):
    driver.find_element(By.ID,"ont_multicast_maxmessage_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"ont_multicast_maxmessage_text").send_keys(value)

def Multicast_Profile_New_Apply(driver):
    Save(driver)

# def Multicast_Profile_New_Delete(driver):
#     driver.find_elements(By.CLASS_NAME, "ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-text-only")[1].click()

# Uni Profile

def Uni_Profile_New(driver):
    New_Profile(driver)

def Uni_Profile_Delete(driver):
    Delete_Profile(driver)

# def Uni_Profile_Delete_All_Select(driver,request):
#     check_box = driver.find_element(By.NAME, "rpXGSponUniProf_chkDelall") 
#     if(check_box.is_selected() == True):
#         if(request == False):
#             check_box.click()
#     else:
#         if(request == True):
#             check_box.click()

# def Uni_Profile_Delete_Select(driver,index):
#     driver.find_elements(By.NAME, "rpXGSponUniProf_chkDel")[index-1].click()

def Uni_Profile_New_Apply(driver):
    Save(driver)

# def Uni_Profile_New_Delete(driver):
#     driver.find_elements(By.CLASS_NAME, "ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-text-only")[1].click()

# # Uni Profile -> Lan

def Uni_Profile_New_Name(driver,value):
    Profile_Name(driver,value)

def Uni_Profile_New_Lan_Vlan_Active(driver,num,request):
    # check_box = driver.find_element(By.XPATH,f'//*[@for="ont_uni_lanportvlan_enable_checkbox{num}"]') ###8
    # if(check_box.is_selected() == True):
    #     if(request == False):
    #         check_box.click()
    # else:
    #     if(request == True):
    #         check_box.click()
    Checkbox_EMS(driver,f'ont_uni_lanportvlan_enable_checkbox{num}',request)

def Uni_Profile_New_Lan_Filter_ethertype(driver,num):
    # driver.find_element(By.ID,f"rpXGSponUniProf_lantagfilter")[3*(num-1)].click()
    # driver.find_element(By.ID,f"ont_uni_lanportvlan_ethertype_combobox{num}").click()
    # driver.find_element(By.XPATH,f'//*[@for="ont_uni_lanportvlan_ethertype_checkbox{num}"]').click()
    Checkbox_EMS(driver,f'ont_uni_lanportvlan_ethertype_checkbox{num}',True)


def Uni_Profile_New_Lan_Filter_ethertype_Value(driver,num,text):
# 第二種寫法 
# if(num == 0):
#     Select(driver.find_element(By.ID, "rpXGSponUniProf_lantagfilterether")).select_by_visible_text(text) #只能是第0個
# else:
#     Select(driver.find_elements(By.ID, "rpXGSponUniProf_lantagfilterether")[num-1]).select_by_visible_text(text)
# 第三種寫法 
# a = driver.find_elements(By.ID, "rpXGSponUniProf_lantagfilterether")[0]
# Select(a).select_by_visible_text("ipoe")
    # Select(driver.find_elements(By.ID, "rpXGSponUniProf_lantagfilterether")[num-1]).select_by_visible_text(text)

    if(text == 'ipoe'):
        text = 'IPoE'
    elif(text == 'arp'):
        text = 'ARP'
    elif(text == 'pppoe'):
        text = 'PPPoE'
    elif(text == 'ipv6'):
        text = 'IPv6'
    Select(driver.find_element(By.ID,f"ont_uni_lanportvlan_ethertype_combobox{num}")).select_by_visible_text(text)


def Uni_Profile_New_Lan_Filter_uniVlan(driver,num):
    # driver.find_element(By.ID,f"rpXGSponUniProf_lantagfilter")[3*(num-1)+1].click()
    # driver.find_element(By.ID,f"rpXGSponUniProf_lantag_unvlan_filter")[num-1].click()
    # driver.find_element(By.XPATH,f'//*[@for="ont_uni_lanportvlan_univlan_checkbox{num}"]').click()
    Checkbox_EMS(driver,f'ont_uni_lanportvlan_univlan_checkbox{num}',True)
    

def Uni_Profile_New_Lan_Filter_uniVlan_Value(driver,num,value):
    driver.find_element(By.ID,f"ont_uni_lanportvlan_univlan_text{num}").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,f"ont_uni_lanportvlan_univlan_text{num}").send_keys(value)
    

def Uni_Profile_New_Lan_Filter_untag(driver,num):
    # driver.find_element(By.ID,f"rpXGSponUniProf_lantagfilter")[3*(num-1)+2].click()
    # driver.find_element(By.ID,f"rpXGSponUniProf_lantag_untag_filter{num}").click()
    time.sleep(1)
    # driver.find_element(By.XPATH,f'//*[@for="ont_uni_lanportvlan_untag_checkbox{num}"]').click()
    Checkbox_EMS(driver,f'ont_uni_lanportvlan_untag_checkbox{num}',True)
    time.sleep(1)

def Uni_Profile_New_Lan_UniportList(driver,num,value):
    driver.find_element(By.ID,f"ont_uni_lanportvlan_uniport_text{num}").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,f"ont_uni_lanportvlan_uniport_text{num}").send_keys(value)

def Uni_Profile_New_Lan_Vlan(driver,num,value):
    driver.find_element(By.ID,f"ont_uni_lanportvlan_vlan_text{num}").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,f"ont_uni_lanportvlan_vlan_text{num}").send_keys(value)   

def Uni_Profile_New_Lan_Active_all(driver,request):
    Checkbox_EMS(driver,f'ont_uni_lanport_enable_checkboxall',request)

def Uni_Profile_New_Lan_Active(driver,num,request):
    Checkbox_EMS(driver,f'ont_uni_lanport_enable_checkbox{num}',request)

def Uni_Profile_New_Lan_fdb_count_all(driver,value):
    driver.find_element(By.ID,"ont_uni_lanport_maxfdb_textall").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"ont_uni_lanport_maxfdb_textall").send_keys(value) 

def Uni_Profile_New_Lan_DS_rate_all(driver,value):
    driver.find_element(By.ID,"ont_uni_lanport_ratelimit_textall").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"ont_uni_lanport_ratelimit_textall").send_keys(value) 

def Uni_Profile_New_Lan_Storm_B_all(driver,value):
    driver.find_element(By.ID,"ont_uni_lanport_broadcast_textall").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"ont_uni_lanport_broadcast_textall").send_keys(value) 

def Uni_Profile_New_Lan_Storm_M_all(driver,value):
    driver.find_element(By.ID,"ont_uni_lanport_multicast_textall").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"ont_uni_lanport_multicast_textall").send_keys(value) 

def Uni_Profile_New_Lan_Storm_D_all(driver,value):
    driver.find_element(By.ID,"ont_uni_lanport_dlf_textall").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"ont_uni_lanport_dlf_textall").send_keys(value) 


# Uni Profile -> XLan

def Uni_Profile_New_Xlan_Enable_10G_BASET_Ethernet_LAN_interface(driver,request):
    Checkbox_EMS(driver,'ont_uni_xlanport_interface_enable_checkbox',request)

def Uni_Profile_New_XLan_Vlan_Active(driver,num,request):
    # check_box = driver.find_element(By.XPATH,f'//*[@for="ont_uni_xlanportvlan_enable_checkbox{num}"]')  ###8
    # if(check_box.is_selected() == True):
    #     if(request == False):
    #         check_box.click()
    # else:
    #     if(request == True):
    #         check_box.click()
    Checkbox_EMS(driver,f'ont_uni_xlanportvlan_enable_checkbox{num}',request)

def Uni_Profile_New_XLan_Filter_ethertype(driver,num):
    # driver.find_element(By.ID,f"rpXGSponUniProf_xlantagfilter")[3*(num-1)].click()
    # driver.find_element(By.ID,f"rpXGSponUniProf_xlantag_ethertype_filter{num}").click()
    # driver.find_element(By.XPATH,f'//*[@for="ont_uni_xlanportvlan_ethertype_checkbox{num}"]').click()
    Checkbox_EMS(driver,f'ont_uni_xlanportvlan_ethertype_checkbox{num}',True)

def Uni_Profile_New_XLan_Filter_ethertype_Value(driver,num,text):
    if(text == 'ipoe'):
        text = 'IPoE'
    elif(text == 'arp'):
        text = 'ARP'
    elif(text == 'pppoe'):
        text = 'PPPoE'
    elif(text == 'ipv6'):
        text = 'IPv6'
    Select(driver.find_element(By.ID,f"ont_uni_xlanportvlan_ethertype_combobox{num}")).select_by_visible_text(text)

def Uni_Profile_New_XLan_Filter_uniVlan(driver,num):
    # driver.find_element(By.ID,f"rpXGSponUniProf_xlantagfilter")[3*(num-1)+1].click()
    # driver.find_element(By.ID,f"rpXGSponUniProf_xlantag_unvlan_filter{num}").click()
    # driver.find_element(By.XPATH,f'//*[@for="ont_uni_xlanportvlan_univlan_checkbox{num}"]').click()
    Checkbox_EMS(driver,f'ont_uni_xlanportvlan_univlan_checkbox{num}',True)

def Uni_Profile_New_XLan_Filter_uniVlan_Value(driver,num,value):
    driver.find_element(By.ID,f"ont_uni_xlanportvlan_univlan_text{num}").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,f"ont_uni_xlanportvlan_univlan_text{num}").send_keys(value)

def Uni_Profile_New_XLan_Filter_untag(driver,num):
    # driver.find_element(By.ID,f"rpXGSponUniProf_xlantagfilter")[3*(num-1)+2].click()
    # driver.find_element(By.ID,f"rpXGSponUniProf_xlantag_untag_filter{num}").click()
    # driver.find_element(By.XPATH,f'//*[@for="ont_uni_xlanportvlan_untag_checkbox{num}"]').click()
    Checkbox_EMS(driver,f'ont_uni_xlanportvlan_untag_checkbox{num}',True)

def Uni_Profile_New_XLan_UniportList(driver,num,value):
    driver.find_element(By.ID,f"ont_uni_xlanportvlan_uniport_text{num}").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,f"ont_uni_xlanportvlan_uniport_text{num}").send_keys(value)

def Uni_Profile_New_XLan_Vlan(driver,num,value):
    driver.find_element(By.ID,f"ont_uni_xlanportvlan_vlan_text{num}").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,f"ont_uni_xlanportvlan_vlan_text{num}").send_keys(value)   

#

def Uni_Profile_New_XLan_Active_all(driver,request):
    Checkbox_EMS(driver,f'ont_uni_xlanport_enable_checkboxall',request)

def Uni_Profile_New_XLan_fdb_count_all(driver,value):
    driver.find_element(By.ID,"ont_uni_xlanport_maxfdb_textall").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"ont_uni_xlanport_maxfdb_textall").send_keys(value) 

def Uni_Profile_New_XLan_DS_rate_all(driver,value):
    driver.find_element(By.ID,"ont_uni_xlanport_ratelimit_textall").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"ont_uni_xlanport_ratelimit_textall").send_keys(value) 

def Uni_Profile_New_XLan_Storm_B_all(driver,value):
    driver.find_element(By.ID,"ont_uni_xlanport_broadcast_textall").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"ont_uni_xlanport_broadcast_textall").send_keys(value) 

def Uni_Profile_New_XLan_Storm_M_all(driver,value):
    driver.find_element(By.ID,"ont_uni_xlanport_multicast_textall").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"ont_uni_xlanport_multicast_textall").send_keys(value) 

def Uni_Profile_New_XLan_Storm_D_all(driver,value):
    driver.find_element(By.ID,"ont_uni_xlanport_dlf_textall").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"ont_uni_xlanport_dlf_textall").send_keys(value) 


# Uni Profile -> Veip
def Uni_Profile_New_Veip_Enable_Virtual_Ethernet_Interface_Point(driver,request):
    Checkbox_EMS(driver,'ont_uni_veipport_interface_enable_checkbox',request) 

def Uni_Profile_New_Veip_Vlan_Active(driver,num,request):
    # check_box = driver.find_element(By.XPATH,f'//*[@for="ont_uni_veipportvlan_enable_checkbox{num}"]')  
    # if(check_box.is_selected() == True):
    #     if(request == False):
    #         check_box.click()
    # else:
    #     if(request == True):
    #         check_box.click()
    Checkbox_EMS(driver,f'ont_uni_veipportvlan_enable_checkbox{num}',request) 

def Uni_Profile_New_Veip_Filter_ethertype(driver,num):
    # driver.find_element(By.ID,f"rpXGSponUniProf_veiptagfilter")[3*(num-1)].click()    
    # driver.find_element(By.XPATH,f'//*[@for="ont_uni_veipportvlan_ethertype_checkbox{num}"]').click()
    Checkbox_EMS(driver,f'ont_uni_veipportvlan_ethertype_checkbox{num}',True)


def Uni_Profile_New_Veip_Filter_ethertype_Value(driver,num,text):
    if(text == 'ipoe'):
        text = 'IPoE'
    elif(text == 'arp'):
        text = 'ARP'
    elif(text == 'pppoe'):
        text = 'PPPoE'
    elif(text == 'ipv6'):
        text = 'IPv6'
    Select(driver.find_element(By.ID,f"ont_uni_veipportvlan_ethertype_combobox{num}")).select_by_visible_text(text)

def Uni_Profile_New_Veip_Filter_uniVlan(driver,num):
    # driver.find_element(By.ID,f"rpXGSponUniProf_veiptagfilter")[3*(num-1)+1].click()
    # driver.find_element(By.XPATH,f'ont_uni_veipportvlan_univlan_checkbox{num}').click()
    Checkbox_EMS(driver,f'ont_uni_veipportvlan_univlan_checkbox{num}',True)

def Uni_Profile_New_Veip_Filter_uniVlan_Value(driver,num,value):
    driver.find_element(By.ID,f"ont_uni_veipportvlan_univlan_text{num}").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,f"ont_uni_veipportvlan_univlan_text{num}").send_keys(value)

def Uni_Profile_New_Veip_Filter_untag(driver,num):
    # driver.find_element(By.ID,f"rpXGSponUniProf_veiptagfilter")[3*(num-1)+2].click()
    # driver.find_element(By.ID,f"rpXGSponUniProf_veiptag_untag_filter{num}").click()
    # driver.find_element(By.XPATH,f'//*[@for="ont_uni_veipportvlan_untag_checkbox{num}"]').click()
    Checkbox_EMS(driver,f'ont_uni_veipportvlan_untag_checkbox{num}',True)

def Uni_Profile_New_Veip_UniportList(driver,num,value):
    driver.find_element(By.ID,f"ont_uni_veipportvlan_uniport_text{num}").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,f"ont_uni_veipportvlan_uniport_text{num}").send_keys(value)

def Uni_Profile_New_Veip_Vlan(driver,num,value):
    driver.find_element(By.ID,f"ont_uni_veipportvlan_vlan_text{num}").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,f"ont_uni_veipportvlan_vlan_text{num}").send_keys(value)   

def Uni_Profile_New_Veip_Active(driver,num,request):
    Checkbox_EMS(driver,f'ont_uni_veipport_enable_checkbox{str(num)}',request)

def Uni_Profile_New_Veip_fdb_count(driver,num,value):
    driver.find_element(By.ID,f"ont_uni_veipport_maxfdb_text{num}").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,f"ont_uni_veipport_maxfdb_text{num}").send_keys(value) 

def Uni_Profile_New_Veip_DS_rate(driver,num,value):
    driver.find_element(By.ID,f"ont_uni_veipport_ratelimit_text{num}").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,f"ont_uni_veipport_ratelimit_text{num}").send_keys(value) 

def Uni_Profile_New_Veip_Storm_B(driver,num,value):
    driver.find_element(By.ID,f"ont_uni_veipport_broadcast_text{num}").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,f"ont_uni_veipport_broadcast_text{num}").send_keys(value) 

def Uni_Profile_New_Veip_Storm_M(driver,num,value):
    driver.find_element(By.ID,f"ont_uni_veipport_multicast_text{num}").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,f"ont_uni_veipport_multicast_text{num}").send_keys(value) 

def Uni_Profile_New_Veip_Storm_D(driver,num,value):
    driver.find_element(By.ID,f"ont_uni_veipport_dlf_text{num}").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,f"ont_uni_veipport_dlf_text{num}").send_keys(value) 


# # Uni Profile -> Lan port                                                                        # no use ???

# def Uni_Profile_New_Lan_Port_Active(driver,num,request):
#     check_box = driver.find_element(By.XPATH,f'//*[@for="ont_uni_lanport_enable_checkbox{num}"]')  ###8
#     if(check_box.is_selected() == True):
#         if(request == False):
#             check_box.click()
#     else:
#         if(request == True):
#             check_box.click()

# def Uni_Profile_New_Lan_Port_FDB(driver,value):
#     driver.find_element(By.NAME,"rpXGSponUniProf_saLanMaxFdbCnt").clear()
#     driver.find_element(By.NAME,"rpXGSponUniProf_saLanMaxFdbCnt").send_keys(value)

# def Uni_Profile_New_Lan_Port_DS(driver,value):
#     driver.find_element(By.NAME,"rpXGSponUniProf_saLanDsPir").clear()
#     driver.find_element(By.NAME,"rpXGSponUniProf_saLanDsPir").send_keys(value)

# def Uni_Profile_New_Lan_Port_Storm_B(driver,value):
#     driver.find_element(By.NAME,"rpXGSponUniProf_saLanStormBcast").clear()
#     driver.find_element(By.NAME,"rpXGSponUniProf_saLanStormBcast").send_keys(value)

# def Uni_Profile_New_Lan_Port_Storm_M(driver,value):
#     driver.find_element(By.NAME,"rpXGSponUniProf_saLanStormMcast").clear()
#     driver.find_element(By.NAME,"rpXGSponUniProf_saLanStormMcast").send_keys(value)

# def Uni_Profile_New_Lan_Port_Storm_D(driver,value):
#     driver.find_element(By.NAME,"rpXGSponUniProf_saLanStormDlf").clear()
#     driver.find_element(By.NAME,"rpXGSponUniProf_saLanStormDlf").send_keys(value)


# # Uni Profile -> XLan port

# def Uni_Profile_New_XLan_Port_Active(driver,num,request):
#     check_box = driver.find_elements(By.ID, "rpXGSponUniProf_xlantagoperActive")[num]  ###8
#     if(check_box.is_selected() == True):
#         if(request == False):
#             check_box.click()
#     else:
#         if(request == True):
#             check_box.click()

# def Uni_Profile_New_XLan_Port_FDB(driver,value):
#     driver.find_element(By.NAME, "rpXGSponUniProf_saXlanMaxFdbCnt").clear()
#     driver.find_element(By.NAME, "rpXGSponUniProf_saXlanMaxFdbCnt").send_keys(value)

# def Uni_Profile_New_XLan_Port_DS(driver,value):
#     driver.find_element(By.NAME, "rpXGSponUniProf_saXlanDsPir").clear()
#     driver.find_element(By.NAME, "rpXGSponUniProf_saXlanDsPir").send_keys(value)

# def Uni_Profile_New_XLan_Port_Storm_B(driver,value):
#     driver.find_element(By.NAME, "rpXGSponUniProf_saXlanStormBcast").clear()
#     driver.find_element(By.NAME, "rpXGSponUniProf_saXlanStormBcast").send_keys(value)

# def Uni_Profile_New_XLan_Port_Storm_M(driver,value):
#     driver.find_element(By.NAME, "rpXGSponUniProf_saXlanStormMcast").clear()
#     driver.find_element(By.NAME, "rpXGSponUniProf_saXlanStormMcast").send_keys(value)

# def Uni_Profile_New_XLan_Port_Storm_D(driver,value):
#     driver.find_element(By.NAME, "rpXGSponUniProf_saXlanStormDlf").clear()
#     driver.find_element(By.NAME, "rpXGSponUniProf_saXlanStormDlf").send_keys(value)

# # Uni Profile -> Veip port

# def Uni_Profile_New_Veip_Port_Active(driver,num,request):
#     check_box = driver.find_elements(By.ID, "rpXGSponUniProf_xlantagoperActive")[num]  ###8
#     if(check_box.is_selected() == True):
#         if(request == False):
#             check_box.click()
#     else:
#         if(request == True):
#             check_box.click()

# def Uni_Profile_New_Veip_Port_FDB(driver,value):
#     driver.find_element(By.NAME, "rpXGSponUniProf_veipMaxFdbCnt").clear()
#     driver.find_element(By.NAME, "rpXGSponUniProf_veipMaxFdbCnt").send_keys(value)

# def Uni_Profile_New_Veip_Port_DS(driver,value):
#     driver.find_element(By.NAME, "rpXGSponUniProf_veipDsPir").clear()
#     driver.find_element(By.NAME, "rpXGSponUniProf_veipDsPir").send_keys(value)

# def Uni_Profile_New_Veip_Port_Storm_B(driver,value):
#     driver.find_element(By.NAME, "rpXGSponUniProf_veipStormCtrlBcast").clear()
#     driver.find_element(By.NAME, "rpXGSponUniProf_veipStormCtrlBcast").send_keys(value)

# def Uni_Profile_New_Veip_Port_Storm_M(driver,value):
#     driver.find_element(By.NAME, "rpXGSponUniProf_veipStormMcast").clear()
#     driver.find_element(By.NAME, "rpXGSponUniProf_veipStormMcast").send_keys(value)

# def Uni_Profile_New_Veip_Port_Storm_D(driver,value):
#     driver.find_element(By.NAME, "rpXGSponUniProf_veipStormDlf").clear()
#     driver.find_element(By.NAME, "rpXGSponUniProf_veipStormDlf").send_keys(value)

# Security Profile

# ONT Security Profile

def ONT_Security_Profile_Name(driver,text):
    driver.find_element(By.ID,"profile_name").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"profile_name").send_keys(text)

def ONT_Security_Profile_AntiMacSpoofing(driver,request):    
    # check_box = driver.find_element(By.XPATH,'//*[@for="ont_security_ams_enable_checkbox"]')
    # if(check_box.is_selected() == True):
    #     if(request == False):
    #         check_box.click()
    # else:
    #     if(request == True):
    #         check_box.click()
    Checkbox_EMS(driver,'ont_security_ams_enable_checkbox',request)

def ONT_Security_Profile_Max_FDB_Count(driver,val):
    driver.find_element(By.ID,"ont_security_maxfdb_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"ont_security_maxfdb_text").send_keys(val)

# def Security_Profile_New(driver):
#     driver.find_element(By.CLASS_NAME, "font-btn").click()

# def Security_Profile_Delete(driver):
#     driver.find_element(By.NAME, "rpXgponSecuProf_TablebtnDelete").click()

# def Security_Profile_Delete_All_Select(driver,request):
#     check_box = driver.find_element(By.NAME, "rpXGSponMcastProf_chkDelall") ###
#     if(check_box.is_selected() == True):
#         if(request == False):
#             check_box.click()
#     else:
#         if(request == True):
#             check_box.click()

# def Security_Profile_Delete_Select(driver,index):
#     driver.find_elements(By.NAME, "rpXGSponSecuProf_chkDel")[index-1].click()

# def Security_Profile_New_Name(driver,value):
#     driver.find_element(By.ID, "rpXGSponSecuProf_IptProfName").clear()
#     driver.find_element(By.ID, "rpXGSponSecuProf_IptProfName").send_keys(value)

# def Security_Profile_New_anti(driver,request):
#     check_box = driver.find_element(By.NAME, "rpXGSponSecuProf_antiMacSpoofing")
#     if(check_box.is_selected() == True):
#         if(request == False):
#             check_box.click()
#     else:
#         if(request == True):
#             check_box.click()

# def Security_Profile_New_fdb(driver,value):
#     driver.find_element(By.ID, "rpXGSponSecuProf_maxFdbCnt").clear()
#     driver.find_element(By.ID, "rpXGSponSecuProf_maxFdbCnt").send_keys(value)

# def Security_Profile_New_Apply(driver):
#     driver.find_elements(By.CLASS_NAME, "ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-text-only")[0].click()

# def Security_Profile_New_Delete(driver):
#     driver.find_elements(By.CLASS_NAME, "ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-text-only")[1].click()


# Ont Profile

def Ont_Profile_New(driver):
    New_Profile(driver)

def Ont_Profile_Delete(driver):
    Delete_Profile(driver)

# def Ont_Profile_Delete_All_Select(driver,request):
#     check_box = driver.find_element(By.NAME, "rpXGSponMcastProf_chkDelall")
#     if(check_box.is_selected() == True):
#         if(request == False):
#             check_box.click()
#     else:
#         if(request == True):
#             check_box.click()

# def Ont_Profile_Delete_Select(driver,index):
#     driver.find_elements(By.NAME, "rpXGSponOntProf_chkDel")[index-1].click()

def Ont_Profile_New_Apply(driver):
    Save(driver)

# def Ont_Profile_New_Delete(driver):
#     driver.find_elements(By.CLASS_NAME, "ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-text-only")[1].click()

# Ont Profile -> Service

def Ont_Profile_New_Name(driver,value):
    Profile_Name(driver,value)

def Ont_Profile_New_Service_Control(driver,request):
    # check_box = driver.find_element(By.XPATH,'//*[@for="ont_ont_service_checkbox"]')
    # if(check_box.is_selected() == True):
    #     if(request == False):
    #         check_box.click()
    # else:
    #     if(request == True):
    #         check_box.click()
    Checkbox_EMS(driver,f'ont_ont_service_checkbox',request)

def Ont_Profile_New_Service_lcmp_enable(driver,text):
    if(text == 'L&W'):
        text = 'LAN and WAN'
    Select(driver.find_element(By.ID,"ont_ont_lcmp_combobox")).select_by_visible_text(text)

def Ont_Profile_New_Service_ftp_enable(driver,text):
    if(text == 'L&W'):
        text = 'LAN and WAN'
    Select(driver.find_element(By.ID,"ont_ont_ftp_combobox")).select_by_visible_text(text)

def Ont_Profile_New_Service_Http_enable(driver,text):
    if(text == 'L&W'):
        text = 'LAN and WAN'
    Select(driver.find_element(By.ID,"ont_ont_http_combobox")).select_by_visible_text(text)

def Ont_Profile_New_Service_Https_enable(driver,text):
    if(text == 'L&W'):
        text = 'LAN and WAN'
    Select(driver.find_element(By.ID,"ont_ont_https_combobox")).select_by_visible_text(text)

def Ont_Profile_New_Service_Snmp_enable(driver,text):
    if(text == 'L&W'):
        text = 'LAN and WAN'
    Select(driver.find_element(By.ID,"ont_ont_snmp_combobox")).select_by_visible_text(text)

def Ont_Profile_New_Service_Telnet_enable(driver,text):
    if(text == 'L&W'):
        text = 'LAN and WAN'
    Select(driver.find_element(By.ID,"ont_ont_telnet_combobox")).select_by_visible_text(text)

def Ont_Profile_New_Service_SSH_enable(driver,text):
    if(text == 'L&W'):
        text = 'LAN and WAN'
    Select(driver.find_element(By.ID,"ont_ont_ssh_combobox")).select_by_visible_text(text)

def Ont_Profile_New_Service_Firewall_control(driver,request):
    # check_box = driver.find_element(By.XPATH,'//*[@for="ont_ont_firewall_checkbox"]')
    # if(check_box.is_selected() == True):
    #     if(request == False):
    #         check_box.click()
    # else:
    #     if(request == True):
    #         check_box.click()
    Checkbox_EMS(driver,f'ont_ont_firewall_checkbox',request)

def Ont_Profile_New_Service_Firewall_enable(driver,text):
    Select(driver.find_element(By.ID,"ont_ont_firewall_combobox")).select_by_visible_text(text)

def Ont_Profile_New_Service_Firewall_level(driver,text):
    text = text.capitalize()
    Select(driver.find_element(By.ID,"ont_ont_firewalllevel_combobox")).select_by_visible_text(text)

def Ont_Profile_New_Service_Dmz_control(driver,request):
    # check_box = driver.find_element(By.XPATH,'//*[@for="ont_ont_dmz_checkbox"]')
    # if(check_box.is_selected() == True):
    #     if(request == False):
    #         check_box.click()
    # else:
    #     if(request == True):
    #         check_box.click()
    Checkbox_EMS(driver,f'ont_ont_dmz_checkbox',request)

def Ont_Profile_New_Service_Dmz_ip(driver,value):
    driver.find_element(By.ID,"ont_ont_dmzip_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"ont_ont_dmzip_text").send_keys(value)

def Ont_Profile_New_Service_PoE_control(driver,request):
    # check_box = driver.find_element(By.XPATH,'//*[@for="ont_ont_poe_checkbox"]')
    # if(check_box.is_selected() == True):
    #     if(request == False):
    #         check_box.click()
    # else:
    #     if(request == True):
    #         check_box.click()
    Checkbox_EMS(driver,f'ont_ont_poe_checkbox',request)

def Ont_Profile_New_Service_PoE_management(driver,text):
    text = text.capitalize()
    Select(driver.find_element(By.ID,"ont_ont_poemanage_combobox")).select_by_visible_text(text)

def Ont_Profile_New_Service_PoE_mode(driver,text):
    text = text.capitalize()
    Select(driver.find_element(By.ID,"ont_ont_poemode_combobox")).select_by_visible_text(text)

def Ont_Profile_New_Service_Upnp_control(driver,request):
    # check_box = driver.find_element(By.XPATH,'//*[@for="ont_ont_upnp_checkbox"]')
    # if(check_box.is_selected() == True):
    #     if(request == False):
    #         check_box.click()
    # else:
    #     if(request == True):
    #         check_box.click()
    Checkbox_EMS(driver,f'ont_ont_upnp_checkbox',request)

def Ont_Profile_New_Service_Upnp_enable(driver,request):
    # check_box = driver.find_element(By.XPATH,'//*[@for="ont_ont_upnpenable_checkbox"]')
    # if(check_box.is_selected() == True):
    #     if(request == False):
    #         check_box.click()
    # else:
    #     if(request == True):
    #         check_box.click()
    Checkbox_EMS(driver,f'ont_ont_upnpenable_checkbox',request)

def Ont_Profile_New_Service_Roaming_control(driver,request):
    # check_box = driver.find_element(By.XPATH,'//*[@for="ont_ont_roaming_checkbox"]')
    # if(check_box.is_selected() == True):
    #     if(request == False):
    #         check_box.click()
    # else:
    #     if(request == True):
    #         check_box.click()
    Checkbox_EMS(driver,f'ont_ont_roaming_checkbox',request)

def Ont_Profile_New_Service_Roaming(driver,value):
    driver.find_element(By.ID,"ont_ont_roaming_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"ont_ont_roaming_text").send_keys(value)

def Ont_Profile_New_Service_Acs_control(driver,request):
    # check_box = driver.find_element(By.XPATH,'//*[@for="ont_ont_acs_checkbox"]')
    # if(check_box.is_selected() == True):
    #     if(request == False):
    #         check_box.click()
    # else:
    #     if(request == True):
    #         check_box.click()
    Checkbox_EMS(driver,f'ont_ont_acs_checkbox',request)

def Ont_Profile_New_Service_Acs_server(driver,request):
    # check_box = driver.find_element(By.XPATH,'//*[@for="ont_ont_acsserver_checkbox"]')
    # if(check_box.is_selected() == True):
    #     if(request == False):
    #         check_box.click()
    # else:
    #     if(request == True):
    #         check_box.click()
    Checkbox_EMS(driver,f'ont_ont_acsserver_checkbox',request)

def Ont_Profile_New_Service_Acs_username(driver,value):
    driver.find_element(By.ID,"ont_ont_acsuser_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"ont_ont_acsuser_text").send_keys(value)

def Ont_Profile_New_Service_Acs_password(driver,value):
    driver.find_element(By.ID,"ont_ont_acspass_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"ont_ont_acspass_text").send_keys(value)

def Ont_Profile_New_Service_Acs_url(driver,value):
    driver.find_element(By.ID,"ont_ont_acsurl_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"ont_ont_acsurl_text").send_keys(value)

def Ont_Profile_New_Service_Acs_inform(driver,request):
    # check_box = driver.find_element(By.XPATH,'//*[@for="ont_ont_acsinform_checkbox"]')
    # if(check_box.is_selected() == True):
    #     if(request == False):
    #         check_box.click()
    # else:
    #     if(request == True):
    #         check_box.click()
    Checkbox_EMS(driver,f'ont_ont_acsinform_checkbox',request)

def Ont_Profile_New_Service_Acs_interval(driver,value):
    driver.find_element(By.ID,"ont_ont_acsinterval_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"ont_ont_acsinterval_text").send_keys(value)

def Ont_Profile_New_Service_Loopguard_control(driver,request):
    # check_box = driver.find_element(By.XPATH,'//*[@for="ont_ont_loopguard_checkbox"]')
    # if(check_box.is_selected() == True):
    #     if(request == False):
    #         check_box.click()
    # else:
    #     if(request == True):
    #         check_box.click()
    Checkbox_EMS(driver,f'ont_ont_loopguard_checkbox',request)

def Ont_Profile_New_Service_Loopguard_detected(driver,value):
    driver.find_element(By.ID,"ont_ont_loopguard_detect_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"ont_ont_loopguard_detect_text").send_keys(value)

def Ont_Profile_New_Service_Loopguard_enable(driver,request):
    # check_box = driver.find_element(By.XPATH,'//*[@for="ont_ont_loopguard_enable_checkbox"]')
    # if(check_box.is_selected() == True):
    #     if(request == False):
    #         check_box.click()
    # else:
    #     if(request == True):
    #         check_box.click()
    Checkbox_EMS(driver,f'ont_ont_loopguard_enable_checkbox',request)

def Ont_Profile_New_Service_Loopguard_recovery(driver,value):
    driver.find_element(By.ID,"ont_ont_loopguard_recovery_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"ont_ont_loopguard_recovery_text").send_keys(value)

def Ont_Profile_New_Service_StormControl_control(driver,request):
    # check_box = driver.find_element(By.XPATH,'//*[@for="ont_ont_storm_checkbox"]')
    # if(check_box.is_selected() == True):
    #     if(request == False):
    #         check_box.click()
    # else:
    #     if(request == True):
    #         check_box.click()
    Checkbox_EMS(driver,f'ont_ont_storm_checkbox',request)

def Ont_Profile_New_Service_StormControl_threshold(driver,value):
    # Storm Control Enable
    Checkbox_EMS(driver,f'ont_ont_stormenable_checkbox',True)
    # Storm Control threshold
    driver.find_element(By.ID,"ont_ont_storm_threshold_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"ont_ont_storm_threshold_text").send_keys(value)

# # Ont Profile -> Lan

def Ont_Profile_New_Lan_Active(driver,index,request):
    # check_box = driver.find_element(By.XPATH,f'//*[@for="ont_ont_lan_enable_checkbox{index}"]')
    # if(check_box.is_selected() == True):
    #     if(request == False):
    #         check_box.click()
    # else:
    #     if(request == True):
    #         check_box.click()
    Checkbox_EMS(driver,f'ont_ont_lan_enable_checkbox{index}',request)

def Ont_Profile_New_Lan_Static_Mode(driver,index,request):
    # check_box = driver.find_element(By.XPATH,f'//*[@for="ont_ont_lan_staticmode_checkbox{index}"]')
    # if(check_box.is_selected() == True):
    #     if(request == False):
    #         check_box.click()
    # else:
    #     if(request == True):
    #         check_box.click()
    Checkbox_EMS(driver,f'ont_ont_lan_staticmode_checkbox{index}',request)

def Ont_Profile_New_Lan_IP(driver,index,value):
    driver.find_element(By.ID,f"ont_ont_lan_ip_text{index}").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,f"ont_ont_lan_ip_text{index}").send_keys(value)

def Ont_Profile_New_Lan_Mask(driver,index,value):
    driver.find_element(By.ID,f"ont_ont_lan_mask_text{index}").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,f"ont_ont_lan_mask_text{index}").send_keys(value)

def Ont_Profile_New_Lan_DHCP_Mode(driver,index,text):
    Select(driver.find_element(By.ID,f"ont_ont_lan_dhcpmode_combobox{index}")).select_by_visible_text(text)

def Ont_Profile_New_Lan_PoolBegin(driver,index,value):
    driver.find_element(By.ID,f"ont_ont_lan_poolbegin_text{index}").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,f"ont_ont_lan_poolbegin_text{index}").send_keys(value)

def Ont_Profile_New_Lan_PoolEnd(driver,index,value):
    driver.find_element(By.ID,f"ont_ont_lan_poolend_text{index}").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,f"ont_ont_lan_poolend_text{index}").send_keys(value)

def Ont_Profile_New_Lan_RelayServerIp(driver,index,value):
    driver.find_element(By.ID,f"ont_ont_lan_relayip_text{index}").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,f"ont_ont_lan_relayip_text{index}").send_keys(value)

def Ont_Profile_New_Lan_DnsType(driver,index,text):
    if(text != "ISP"):
        text = text.capitalize()
    Select(driver.find_element(By.ID,f"ont_ont_lan_dnstype_combobox{index}")).select_by_visible_text(text)

def Ont_Profile_New_Lan_priDns(driver,index,value):
    driver.find_element(By.ID,f"ont_ont_lan_pridns_text{index}").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,f"ont_ont_lan_pridns_text{index}").send_keys(value)

def Ont_Profile_New_Lan_secDns(driver,index,value):
    driver.find_element(By.ID,f"ont_ont_lan_secdns_text{index}").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,f"ont_ont_lan_secdns_text{index}").send_keys(value)

# # Ont Profile -> Wan

def Ont_Profile_New_Wan_Active(driver,index,request):
    # check_box = driver.find_element(By.XPATH,f'//*[@for="ont_ont_wan_active_checkbox{index}"]')
    # if(check_box.is_selected() == True):
    #     if(request == False):
    #         check_box.click()
    # else:
    #     if(request == True):
    #         check_box.click()
    Checkbox_EMS(driver,f'ont_ont_wan_active_checkbox{index}',request)

def Ont_Profile_New_Wan_Default(driver,index,request):
    # check_box = driver.find_element(By.XPATH,f'//*[@for="ont_ont_wan_default_checkbox{index}"]')
    # if(check_box.is_selected() == True):
    #     if(request == False):
    #         check_box.click()
    # else:
    #     if(request == True):
    #         check_box.click()
    Checkbox_EMS(driver,f'ont_ont_wan_default_checkbox{index}',request)

def Ont_Profile_New_Wan_Enable(driver,index,request):
    # check_box = driver.find_element(By.XPATH,f'//*[@for="ont_ont_wan_enable_checkbox{index}"]')
    # if(check_box.is_selected() == True):
    #     if(request == False):
    #         check_box.click()
    # else:
    #     if(request == True):
    #         check_box.click()
    Checkbox_EMS(driver,f'ont_ont_wan_enable_checkbox{index}',request)

def Ont_Profile_New_Wan_Nat(driver,index,request):
    # check_box = driver.find_element(By.XPATH,f'//*[@for="ont_ont_wan_ipnat_checkbox{index}"]')
    # if(check_box.is_selected() == True):
    #     if(request == False):
    #         check_box.click()
    # else:
    #     if(request == True):
    #         check_box.click()
    Checkbox_EMS(driver,f'ont_ont_wan_ipnat_checkbox{index}',request)

def Ont_Profile_New_Wan_Mode(driver,index,text):
    text = text.capitalize()
    Select(driver.find_element(By.ID,f"ont_ont_wan_ipmode_combobox{index}")).select_by_visible_text(text)

def Ont_Profile_New_Wan_Address(driver,index,value):
    driver.find_element(By.ID,f"ont_ont_wan_ipstatic_ip_text{index}").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,f"ont_ont_wan_ipstatic_ip_text{index}").send_keys(value)

def Ont_Profile_New_Wan_Mask(driver,index,value):
    driver.find_element(By.ID,f"ont_ont_wan_ipstatic_mask_text{index}").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,f"ont_ont_wan_ipstatic_mask_text{index}").send_keys(value)

def Ont_Profile_New_Wan_Gateway(driver,index,value):
    driver.find_element(By.ID,f"ont_ont_wan_ipstatic_gateway_text{index}").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,f"ont_ont_wan_ipstatic_gateway_text{index}").send_keys(value)

def Ont_Profile_New_Wan_priDns(driver,index,value):
    time.sleep(1)
    driver.find_element(By.ID,f"ont_ont_wan_dynamic_pridns_text{index}").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,f"ont_ont_wan_dynamic_pridns_text{index}").send_keys(value)

def Ont_Profile_New_Wan_secDns(driver,index,value):
    time.sleep(1)
    driver.find_element(By.ID,f"ont_ont_wan_dynamic_pridns_secdns_text{index}").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,f"ont_ont_wan_dynamic_pridns_secdns_text{index}").send_keys(value)
#
def Ont_Profile_New_Wan_type(driver,index,text):
    if(text == 'ipoe'):
        text = 'IPoE'
    elif(text == 'arp'):
        text = 'ARP'
    elif(text == 'pppoe'):
        text = 'PPPoE'
    elif(text == 'ipv6'):
        text = 'IPv6'
    elif(text == 'bridge'):
        text = 'Bridge'
    Select(driver.find_element(By.ID,f"ont_ont_wan_connect_type_combobox{index}")).select_by_visible_text(text)

def Ont_Profile_New_Wan_username(driver,index,value):
    driver.find_element(By.ID,f"ont_ont_wan_user_text{index}").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,f"ont_ont_wan_user_text{index}").send_keys(value)

def Ont_Profile_New_Wan_password(driver,index,value):
    driver.find_element(By.ID,f"ont_ont_wan_pass_text{index}").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,f"ont_ont_wan_pass_text{index}").send_keys(value)

def Ont_Profile_New_Wan_port_list(driver,index,value):
    driver.find_element(By.ID,f"ont_ont_wan_bind_portlist_text{index}").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,f"ont_ont_wan_bind_portlist_text{index}").send_keys(value)

def Ont_Profile_New_Wan_wifi_2_4_ssid(driver,index,value):
    driver.find_element(By.ID,f"ont_ont_wan_bind_24ssid_text{index}").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,f"ont_ont_wan_bind_24ssid_text{index}").send_keys(value)

def Ont_Profile_New_Wan_wifi_5_ssid(driver,index,value):
    driver.find_element(By.ID,f"ont_ont_wan_bind_5ssid_text{index}").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,f"ont_ont_wan_bind_5ssid_text{index}").send_keys(value)

def Ont_Profile_New_Wan_vlan(driver,index,value):
    driver.find_element(By.ID,f"ont_ont_wan_vlan_text{index}").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,f"ont_ont_wan_vlan_text{index}").send_keys(value)


def Ont_Profile_New_Wan_priority(driver,index,text):
    Select(driver.find_element(By.ID,f"ont_ont_wan_pri_combobox{index}")).select_by_visible_text(text)

def Ont_Profile_New_Wan_mvlan(driver,index,value):
    driver.find_element(By.ID,f"ont_ont_wan_mvlan_text{index}").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,f"ont_ont_wan_mvlan_text{index}").send_keys(value)

def Ont_Profile_New_Wan_service(driver,index,value):
    driver.find_element(By.ID,f"ont_ont_wan_service_text{index}").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,f"ont_ont_wan_service_text{index}").send_keys(value)


# Ont Profile -> WiFi 2.4g

def Ont_Profile_New_WiFi_2_4g_Active(driver,index,request):
    # check_box = driver.find_element(By.XPATH,f'//*[@for="ont_ont_wifi24g_active_checkbox{index}"]')
    # if(check_box.is_selected() == True):
    #     if(request == False):
    #         check_box.click()
    # else:
    #     if(request == True):
    #         check_box.click()
    Checkbox_EMS(driver,f'ont_ont_wifi24g_active_checkbox{index}',request)

def Ont_Profile_New_WiFi_2_4g_Enable(driver,index,text):
    # check_box = driver.find_element(By.XPATH,f'//*[@for="ont_ont_wifi24g_enable_checkbox{index}"]')
    # if(check_box.is_selected() == True):
    #     if(request == False):
    #         check_box.click()
    # else:
    #     if(request == True):
    #         check_box.click()
    # Checkbox_EMS(driver,f'ont_ont_wifi24g_enable_checkbox{index}',request)
    Select(driver.find_element(By.ID,f"ont_ont_wifi24g_enable_checkbox{index}")).select_by_visible_text(text)

def Ont_Profile_New_WiFi_2_4g_ssid(driver,index,value):
    driver.find_element(By.ID,f"ont_ont_wifi24g_ssid_text{index}").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,f"ont_ont_wifi24g_ssid_text{index}").send_keys(value)

def Ont_Profile_New_WiFi_2_4g_password(driver,index,value):
    driver.find_element(By.ID,f"ont_ont_wifi24g_password_text{index}").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,f"ont_ont_wifi24g_password_text{index}").send_keys(value)

def Ont_Profile_New_WiFi_2_4g_securityMode(driver,index,text):
    Select(driver.find_element(By.ID,f"ont_ont_wifi24g_security_mode_combobox{index}")).select_by_visible_text(text)

def Ont_Profile_New_WiFi_2_4g_Channel(driver,index,text):
    Select(driver.find_element(By.ID,f"ont_ont_wifi24g_channel_combobox{index}")).select_by_visible_text(text)

def Ont_Profile_New_WiFi_2_4g_Bandwidth(driver,index,text):
    Select(driver.find_element(By.ID,f"ont_ont_wifi24g_bandwidth_combobox{index}")).select_by_visible_text(text)

def Ont_Profile_New_WiFi_2_4g_maxClients(driver,index,value):
    driver.find_element(By.ID,f"ont_ont_wifi24g_maxclient_text{index}").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,f"ont_ont_wifi24g_maxclient_text{index}").send_keys(value)

def Ont_Profile_New_WiFi_2_4g_txPower(driver,index,text):
    Select(driver.find_element(By.ID,f"ont_ont_wifi24g_txpower_combobox{index}")).select_by_visible_text(text)


# Ont Profile -> WiFi 5g

def Ont_Profile_New_WiFi_5g_Active(driver,index,request):
    # check_box = driver.find_element(By.XPATH,f'//*[@for="ont_ont_wifi5g_active_checkbox{index}"]')
    # if(check_box.is_selected() == True):
    #     if(request == False):
    #         check_box.click()
    # else:
    #     if(request == True):
    #         check_box.click()
    Checkbox_EMS(driver,f'ont_ont_wifi5g_active_checkbox{index}',request)

def Ont_Profile_New_WiFi_5g_Enable(driver,index,text):
    # check_box = driver.find_element(By.XPATH,f'//*[@for="ont_ont_wifi5g_enable_checkbox{index}"]')
    # if(check_box.is_selected() == True):
    #     if(request == False):
    #         check_box.click()
    # else:
    #     if(request == True):
    #         check_box.click()
    # Checkbox_EMS(driver,f'ont_ont_wifi5g_enable_checkbox{index}',request)
    Select(driver.find_element(By.ID,f"ont_ont_wifi5g_enable_checkbox{index}")).select_by_visible_text(text)

def Ont_Profile_New_WiFi_5g_ssid(driver,index,value):
    driver.find_element(By.ID,f"ont_ont_wifi5g_ssid_text{index}").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,f"ont_ont_wifi5g_ssid_text{index}").send_keys(value)

def Ont_Profile_New_WiFi_5g_password(driver,index,value):
    driver.find_element(By.ID,f"ont_ont_wifi5g_password_text{index}").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,f"ont_ont_wifi5g_password_text{index}").send_keys(value)

def Ont_Profile_New_WiFi_5g_securityMode(driver,index,text):
    Select(driver.find_element(By.ID,f"ont_ont_wifi5g_security_mode_combobox{index}")).select_by_visible_text(text)

def Ont_Profile_New_WiFi_5g_Channel(driver,index,text):
    Select(driver.find_element(By.ID,f"ont_ont_wifi5g_channel_combobox{index}")).select_by_visible_text(text)

def Ont_Profile_New_WiFi_5g_Bandwidth(driver,index,text):
    Select(driver.find_element(By.ID,f"ont_ont_wifi5g_bandwidth_combobox{index}")).select_by_visible_text(text)

def Ont_Profile_New_WiFi_5g_maxClients(driver,index,value):
    driver.find_element(By.ID,f"ont_ont_wifi5g_maxclient_text{index}").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,f"ont_ont_wifi5g_maxclient_text{index}").send_keys(value)

def Ont_Profile_New_WiFi_5g_txPower(driver,index,text):
    Select(driver.find_element(By.ID,f"ont_ont_wifi5g_txpower_combobox{index}")).select_by_visible_text(text)

# Ont Profile -> Acl

def Ont_Profile_New_Acl_Active(driver,index,request):
    # check_box = driver.find_element(By.XPATH,f'//*[@for="ont_ont_acl_active_checkbox{index}"]')
    # if(check_box.is_selected() == True):
    #     if(request == False):
    #         check_box.click()
    # else:
    #     if(request == True):
    #         check_box.click()
    Checkbox_EMS(driver,f'ont_ont_acl_active_checkbox{index}',request)

def Ont_Profile_New_Acl_Name(driver,index,text):
    Select(driver.find_element(By.ID,f"ont_ont_acl_acl_text{index}")).select_by_visible_text(text)


# Ont Profile -> Voip

def Ont_Profile_New_Voip_Uniport(driver,index,text):
    Select(driver.find_element(By.ID,f"ont_ont_voip_uniport_combobox{index}")).select_by_visible_text(text)

def Ont_Profile_New_Voip_Enable(driver,index,request):
    # check_box = driver.find_element(By.XPATH,f'//*[@for="ont_ont_voip_enable_checkbox{index}"]')
    # if(check_box.is_selected() == True):
    #     if(request == False):
    #         check_box.click()
    # else:
    #     if(request == True):
    #         check_box.click()
    Checkbox_EMS(driver,f'ont_ont_voip_enable_checkbox{index}',request)

def Ont_Profile_New_Voip_Active(driver,index,request):    
    # check_box = driver.find_element(By.XPATH,f'//*[@for="ont_ont_voip_activ_checkbox{index}"]')
    # if(check_box.is_selected() == True):
    #     if(request == False):
    #         check_box.click()
    # else:
    #     if(request == True):
    #         check_box.click()
    Checkbox_EMS(driver,f'ont_ont_voip_activ_checkbox{index}',request)

def Ont_Profile_New_Voip_Vlan(driver,index,value): 
    driver.find_element(By.ID,f"ont_ont_voip_vlan_text{index}").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,f"ont_ont_voip_vlan_text{index}").send_keys(value)
    # driver.find_element(By.XPATH,"//*[@id='rpXGSponVoipVlanId']").clear()
    # driver.find_element(By.XPATH,"//*[@id='rpXGSponVoipVlanId']").send_keys(value)
    # //*[@id="rpXGSponVoipVlanId"]

def Ont_Profile_New_Voip_Username(driver,index,value): 
    driver.find_element(By.ID,f"ont_ont_voip_name_text{index}").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,f"ont_ont_voip_name_text{index}").send_keys(value)
    
def Ont_Profile_New_Voip_Password(driver,index,value):         
    driver.find_element(By.ID,f"ont_ont_voip_password_text{index}").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,f"ont_ont_voip_password_text{index}").send_keys(value)
    
def Ont_Profile_New_Voip_User_Part_AOR(driver,index,value):
    driver.find_element(By.ID,f"ont_ont_voip_aor_text{index}").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,f"ont_ont_voip_aor_text{index}").send_keys(value)
    
def Ont_Profile_New_Voip_Display_Name(driver,index,value):  
    driver.find_element(By.ID,f"ont_ont_voip_displayname_text{index}").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,f"ont_ont_voip_displayname_text{index}").send_keys(value)

def Ont_Profile_New_Voip_Voicemail_Server_SIP_URI(driver,index,value): 
    driver.find_element(By.ID,f"ont_ont_voip_sipuri_text{index}").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,f"ont_ont_voip_sipuri_text{index}").send_keys(value)

def Ont_Profile_New_Voip_Voicemail_Expiration_Time(driver,index,value): 
    driver.find_element(By.ID,f"ont_ont_voip_expiretime_text{index}").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,f"ont_ont_voip_expiretime_text{index}").send_keys(value)

def Ont_Profile_New_Voip_Release_Timer(driver,index,value): 
    driver.find_element(By.ID,f"ont_ont_voip_releasetime_text{index}").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,f"ont_ont_voip_releasetime_text{index}").send_keys(value)

def Ont_Profile_New_Voip_ROH_Timer(driver,index,value):
    driver.find_element(By.ID,f"ont_ont_voip_rohtime_text{index}").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,f"ont_ont_voip_rohtime_text{index}").send_keys(value)

def Ont_Profile_New_Voip_VoIP_Comment_Profile(driver,index,text):
    Select(driver.find_element(By.ID,f"ont_ont_voip_common_combobox{index}")).select_by_visible_text(text)

def Ont_Profile_New_Voip_VoIP_Sip_Profile(driver,index,text):
    Select(driver.find_element(By.ID,f"ont_ont_voip_sip_combobox{index}")).select_by_visible_text(text) 

def Ont_Profile_New_Voip_VoIP_Dial_Plan_Profile(driver,index,text):
    Select(driver.find_element(By.ID,f"ont_ont_voip_dialplan_combobox{index}")).select_by_visible_text(text) 


# Ont Profile -> Poe

def Ont_Profile_New_Poe_Active(driver,index,request):
    # check_box = driver.find_element(By.XPATH,f'//*[@for="ont_ont_poe_active_checkbox{index}"]')
    # if(check_box.is_selected() == True):
    #     if(request == False):
    #         check_box.click()
    # else:
    #     if(request == True):
    #         check_box.click()
    Checkbox_EMS(driver,f'ont_ont_poe_active_checkbox{index}',request)

def Ont_Profile_New_Poe_Enable(driver,index,request):
    # check_box = driver.find_element(By.XPATH,f'//*[@for="ont_ont_poe_enable_checkbox{index}"]')
    # if(check_box.is_selected() == True):
    #     if(request == False):
    #         check_box.click()
    # else:
    #     if(request == True):
    #         check_box.click()
    Checkbox_EMS(driver,f'ont_ont_poe_enable_checkbox{index}',request)

def Ont_Profile_New_Poe_Priority(driver,index,text):
    text = text.capitalize()    
    Select(driver.find_element(By.ID,f"ont_ont_poe_priority_combobox{index}")).select_by_visible_text(text) 

def Ont_Profile_New_Poe_Max(driver,index,text):
    text = text.capitalize()
    Select(driver.find_element(By.ID,f"ont_ont_poe_max_combobox{index}")).select_by_visible_text(text) 



# # Sip Profile

def Sip_Profile_New(driver):
    New_Profile(driver)

def Sip_Profile_Delete(driver):
    Delete_Profile(driver)

# def Sip_Profile_Delete_All_Select(driver,request):
#     check_box = driver.find_element(By.NAME, "rpXGSponMcastProf_chkDelall")
#     if(check_box.is_selected() == True):
#         if(request == False):
#             check_box.click()
#     else:
#         if(request == True):
#             check_box.click()

def Sip_Profile_New_Apply(driver):
    Save(driver)

# def Sip_Profile_New_Delete(driver):
#     driver.find_elements(By.CLASS_NAME, "ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-text-only")[1].click()

def Sip_Profile_New_Name(driver,name):
    Profile_Name(driver,name)

def Sip_Profile_New_PSA(driver,value):
    input = driver.find_element(By.ID,"ont_voip_sip_serviceip_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(value)

def Sip_Profile_New_OPA(driver,value):
    input = driver.find_element(By.ID,"ont_voip_sip_outboundip_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(value)

def Sip_Profile_New_PD(driver,value):
    input = driver.find_element(By.ID,"ont_voip_sip_pri_dns_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(value)

def Sip_Profile_New_SD(driver,value):
    input = driver.find_element(By.ID,"ont_voip_sip_sec_dns_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(value)

def Sip_Profile_New_RET(driver,value):
    input = driver.find_element(By.ID,"ont_voip_sip_extime_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(value)

def Sip_Profile_New_RHST(driver,value):
    input = driver.find_element(By.ID,"ont_voip_sip_start_time_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(value)

def Sip_Profile_New_HPU(driver,value):
    input = driver.find_element(By.ID,"ont_voip_sip_uri_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(value)

def Sip_Profile_New_SR(driver,value):
    input = driver.find_element(By.ID,"ont_voip_sip_registrar_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(value)

def Sip_Profile_New_S(driver,value):
    input = driver.find_element(By.ID,"ont_voip_sip_softswitch_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(value)
    
def Sip_Profile_New_CI_cal_num(driver,request):
    # check_box = driver.find_element(By.XPATH,'//*[@for="ont_voip_sip_caller_calnum_checkbox"]')
    # if(check_box.is_selected() == True):
    #     if(request == False):
    #         check_box.click()
    # else:
    #     if(request == True):
    #         check_box.click()
    Checkbox_EMS(driver,f'ont_voip_sip_caller_calnum_checkbox',request)
    
def Sip_Profile_New_CI_cal_nam(driver,request):
    # check_box = driver.find_element(By.XPATH,'//*[@for="ont_voip_sip_caller_calnam_checkbox"]')
    # if(check_box.is_selected() == True):
    #     if(request == False):
    #         check_box.click()
    # else:
    #     if(request == True):
    #         check_box.click()
    Checkbox_EMS(driver,f'ont_voip_sip_caller_calnam_checkbox',request)
    
def Sip_Profile_New_CI_cid_bio(driver,request):
    # check_box = driver.find_element(By.XPATH,'//*[@for="ont_voip_sip_caller_cidblo_checkbox"]')
    # if(check_box.is_selected() == True):
    #     if(request == False):
    #         check_box.click()
    # else:
    #     if(request == True):
    #         check_box.click()
    Checkbox_EMS(driver,f'ont_voip_sip_caller_cidblo_checkbox',request)
    
def Sip_Profile_New_CI_cid_num(driver,request):
    # check_box = driver.find_element(By.XPATH,'//*[@for="ont_voip_sip_caller_cidnum_checkbox"]')
    # if(check_box.is_selected() == True):
    #     if(request == False):
    #         check_box.click()
    # else:
    #     if(request == True):
    #         check_box.click()
    Checkbox_EMS(driver,f'ont_voip_sip_caller_cidnum_checkbox',request)
    
def Sip_Profile_New_CI_cid_nam(driver,request):
    # check_box = driver.find_element(By.XPATH,'//*[@for="ont_voip_sip_caller_cidnam_checkbox"]')
    # if(check_box.is_selected() == True):
    #     if(request == False):
    #         check_box.click()
    # else:
    #     if(request == True):
    #         check_box.click()
    Checkbox_EMS(driver,f'ont_voip_sip_caller_cidnam_checkbox',request)
    
def Sip_Profile_New_CI_ACR(driver,request):
    # check_box = driver.find_element(By.XPATH,'//*[@for="ont_voip_sip_caller_acr_checkbox"]')
    # if(check_box.is_selected() == True):
    #     if(request == False):
    #         check_box.click()
    # else:
    #     if(request == True):
    #         check_box.click()
    Checkbox_EMS(driver,f'ont_voip_sip_caller_acr_checkbox',request)
    
def Sip_Profile_New_CW_cal_wai(driver,request):
    # check_box = driver.find_element(By.XPATH,'//*[@for="ont_voip_sip_waiting_calwai_checkbox"]')
    # if(check_box.is_selected() == True):
    #     if(request == False):
    #         check_box.click()
    # else:
    #     if(request == True):
    #         check_box.click()
    Checkbox_EMS(driver,f'ont_voip_sip_waiting_calwai_checkbox',request)
    
def Sip_Profile_New_CW_cid_ann(driver,request):
    # check_box = driver.find_element(By.XPATH,'//*[@for="ont_voip_sip_waiting_cidann_checkbox"]')
    # if(check_box.is_selected() == True):
    #     if(request == False):
    #         check_box.click()
    # else:
    #     if(request == True):
    #         check_box.click()
    Checkbox_EMS(driver,f'ont_voip_sip_waiting_cidann_checkbox',request)
    
def Sip_Profile_New_CPOT_3way(driver,request):
    # check_box = driver.find_element(By.XPATH,'//*[@for="ont_voip_sip_progress_3way_checkbox"]')
    # if(check_box.is_selected() == True):
    #     if(request == False):
    #         check_box.click()
    # else:
    #     if(request == True):
    #         check_box.click()
    Checkbox_EMS(driver,f'ont_voip_sip_progress_3way_checkbox',request)
    
def Sip_Profile_New_CPOT_cal_tra(driver,request):
    # check_box = driver.find_element(By.XPATH,'//*[@for="ont_voip_sip_progress_caltra_checkbox"]')
    # if(check_box.is_selected() == True):
    #     if(request == False):
    #         check_box.click()
    # else:
    #     if(request == True):
    #         check_box.click()
    Checkbox_EMS(driver,f'ont_voip_sip_progress_caltra_checkbox',request)
    
def Sip_Profile_New_CPOT_cal_hol(driver,request):
    # check_box = driver.find_element(By.XPATH,'//*[@for="ont_voip_sip_progress_calhol_checkbox"]')
    # if(check_box.is_selected() == True):
    #     if(request == False):
    #         check_box.click()
    # else:
    #     if(request == True):
    #         check_box.click()
    Checkbox_EMS(driver,f'ont_voip_sip_progress_calhol_checkbox',request)
    
def Sip_Profile_New_CPOT_cal_par(driver,request):
    # check_box = driver.find_element(By.XPATH,'//*[@for="ont_voip_sip_progress_calpar_checkbox"]')
    # if(check_box.is_selected() == True):
    #     if(request == False):
    #         check_box.click()
    # else:
    #     if(request == True):
    #         check_box.click()
    Checkbox_EMS(driver,f'ont_voip_sip_progress_calpar_checkbox',request)
    
def Sip_Profile_New_CPOT_not_dis(driver,request):
    # check_box = driver.find_element(By.XPATH,'//*[@for="ont_voip_sip_progress_notdis_checkbox"]')
    # if(check_box.is_selected() == True):
    #     if(request == False):
    #         check_box.click()
    # else:
    #     if(request == True):
    #         check_box.click()
    Checkbox_EMS(driver,f'ont_voip_sip_progress_notdis_checkbox',request)
    
def Sip_Profile_New_CPOT_flash(driver,request):
    # check_box = driver.find_element(By.XPATH,'//*[@for="ont_voip_sip_progress_flash_checkbox"]')
    # if(check_box.is_selected() == True):
    #     if(request == False):
    #         check_box.click()
    # else:
    #     if(request == True):
    #         check_box.click()
    Checkbox_EMS(driver,f'ont_voip_sip_progress_flash_checkbox',request)
    
def Sip_Profile_New_CPOT_origin(driver,request):
    # check_box = driver.find_element(By.XPATH,'//*[@for="ont_voip_sip_progress_origin_checkbox"]')
    # if(check_box.is_selected() == True):
    #     if(request == False):
    #         check_box.click()
    # else:
    #     if(request == True):
    #         check_box.click()
    Checkbox_EMS(driver,f'ont_voip_sip_progress_origin_checkbox',request)
    
def Sip_Profile_New_CPOT_6way(driver,request):
    # check_box = driver.find_element(By.XPATH,'//*[@for="ont_voip_sip_progress_6way_checkbox"]')
    # if(check_box.is_selected() == True):
    #     if(request == False):
    #         check_box.click()
    # else:
    #     if(request == True):
    #         check_box.click()
    Checkbox_EMS(driver,f'ont_voip_sip_progress_6way_checkbox',request)
    
def Sip_Profile_New_CP_spl_rin(driver,request):
    # check_box = driver.find_element(By.XPATH,'//*[@for="ont_voip_sip_presentation_splrin_checkbox"]')
    # if(check_box.is_selected() == True):
    #     if(request == False):
    #         check_box.click()
    # else:
    #     if(request == True):
    #         check_box.click()
    Checkbox_EMS(driver,f'ont_voip_sip_presentation_splrin_checkbox',request)
    
def Sip_Profile_New_CP_dia_ton(driver,request):
    # check_box = driver.find_element(By.XPATH,'//*[@for="ont_voip_sip_presentation_diaton_checkbox"]')
    # if(check_box.is_selected() == True):
    #     if(request == False):
    #         check_box.click()
    # else:
    #     if(request == True):
    #         check_box.click()
    Checkbox_EMS(driver,f'ont_voip_sip_presentation_diaton_checkbox',request)
    
def Sip_Profile_New_CP_vis_ind(driver,request):
    # check_box = driver.find_element(By.XPATH,'//*[@for="ont_voip_sip_presentation_visind_checkbox"]')
    # if(check_box.is_selected() == True):
    #     if(request == False):
    #         check_box.click()
    # else:
    #     if(request == True):
    #         check_box.click()
    Checkbox_EMS(driver,f'ont_voip_sip_presentation_visind_checkbox',request)
    
def Sip_Profile_New_CP_cal_for(driver,request):
    # check_box = driver.find_element(By.XPATH,'//*[@for="ont_voip_sip_presentation_calfor_checkbox"]')
    # if(check_box.is_selected() == True):
    #     if(request == False):
    #         check_box.click()
    # else:
    #     if(request == True):
    #         check_box.click()
    Checkbox_EMS(driver,f'ont_voip_sip_presentation_calfor_checkbox',request)
    
def Sip_Profile_New_DC_enable(driver,request):
    # check_box = driver.find_element(By.XPATH,'//*[@for="ont_voip_sip_connect_enable_checkbox"]')
    # if(check_box.is_selected() == True):
    #     if(request == False):
    #         check_box.click()
    # else:
    #     if(request == True):
    #         check_box.click()
    Checkbox_EMS(driver,f'ont_voip_sip_connect_enable_checkbox',request)
    
def Sip_Profile_New_DC_dia_opt(driver,request):
    # check_box = driver.find_element(By.XPATH,'//*[@for="ont_voip_sip_connect_diaopt_checkbox"]')
    # if(check_box.is_selected() == True):
    #     if(request == False):
    #         check_box.click()
    # else:
    #     if(request == True):
    #         check_box.click()
    Checkbox_EMS(driver,f'ont_voip_sip_connect_diaopt_checkbox',request)

def Sip_Profile_New_DCU(driver,value):
    input = driver.find_element(By.ID,"ont_voip_sip_connecturi_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(value)

def Sip_Profile_New_BLAU(driver,value):
    input = driver.find_element(By.ID,"ont_voip_sip_bridgeduri_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(value)

def Sip_Profile_New_CFU(driver,value):
    input = driver.find_element(By.ID,"ont_voip_sip_conferenceuri_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(value)

# # Voip Common Profile

def Voip_Common_Profile_New(driver):
    New_Profile(driver)

def Voip_Common_Profile_Delete(driver):
    Delete_Profile(driver)

# def Voip_Common_Profile_Delete_All_Select(driver,request):
#     check_box = driver.find_element(By.NAME, "rpXGSponMcastProf_chkDelall")
#     if(check_box.is_selected() == True):
#         if(request == False):
#             check_box.click()
#     else:
#         if(request == True):
#             check_box.click()

def Voip_Common_Profile_New_Apply(driver):
    Save(driver)

# def Voip_Common_Profile_New_Delete(driver):
#     driver.find_elements(By.CLASS_NAME, "ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-text-only")[1].click()

def Voip_Common_Profile_New_Name(driver,name):
    Profile_Name(driver,name)

def Voip_Common_Profile_New_min_Local_Port(driver,vlaue):
    input = driver.find_element(By.ID,"ont_voip_common_minport_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(vlaue)

def Voip_Common_Profile_New_max_Local_Port(driver,vlaue):
    input = driver.find_element(By.ID,"ont_voip_common_maxport_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(vlaue)

def Voip_Common_Profile_New_dscp_mark(driver,vlaue):
    input = driver.find_element(By.ID,"ont_voip_common_dscpmark_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(vlaue)

def Voip_Common_Profile_New_piggyback(driver,request):
    # check_box = driver.find_element(By.XPATH,'//*[@for="ont_voip_common_piggyback_checkbox"]')
    # if(check_box.is_selected() == True):
    #     if(request == False):
    #         check_box.click()
    # else:
    #     if(request == True):
    #         check_box.click()
    Checkbox_EMS(driver,f'ont_voip_common_piggyback_checkbox',request)

def Voip_Common_Profile_New_tone(driver,request):
    # check_box = driver.find_element(By.XPATH,'//*[@for="ont_voip_common_tone_checkbox"]')
    # if(check_box.is_selected() == True):
    #     if(request == False):
    #         check_box.click()
    # else:
    #     if(request == True):
    #         check_box.click()
    Checkbox_EMS(driver,f'ont_voip_common_tone_checkbox',request)

def Voip_Common_Profile_New_dtmf(driver,request):
    # check_box = driver.find_element(By.XPATH,'//*[@for="ont_voip_common_dtmf_checkbox"]')
    # if(check_box.is_selected() == True):
    #     if(request == False):
    #         check_box.click()
    # else:
    #     if(request == True):
    #         check_box.click()
    Checkbox_EMS(driver,f'ont_voip_common_dtmf_checkbox',request)

def Voip_Common_Profile_New_cas(driver,request):
    # check_box = driver.find_element(By.XPATH,'//*[@for="ont_voip_common_cas_checkbox"]')
    # if(check_box.is_selected() == True):
    #     if(request == False):
    #         check_box.click()
    # else:
    #     if(request == True):
    #         check_box.click()
    Checkbox_EMS(driver,f'ont_voip_common_cas_checkbox',request)

def Voip_Common_Profile_New_jitter_target(driver,vlaue):
    input = driver.find_element(By.ID,"ont_voip_common_jitter_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(vlaue)

def Voip_Common_Profile_New_max_jitter_buffer(driver,vlaue):
    input = driver.find_element(By.ID,"ont_voip_common_maxjitter_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(vlaue)

def Voip_Common_Profile_New_ptsn_protocol(driver,vlaue):
    input = driver.find_element(By.ID,"ont_voip_common_pstn_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(vlaue)

def Voip_Common_Profile_New_announce_type(driver,text):
    if(text == 'Voi-ann'):
        text = 'Voice announcement'
    Select(driver.find_element(By.ID,"ont_voip_common_announce_combobox")).select_by_visible_text(text)

def Voip_Common_Profile_New_echo_cancel(driver,request):
    # check_box = driver.find_element(By.XPATH,'//*[@for="ont_voip_common_echo_checkbox"]')
    # if(check_box.is_selected() == True):     
    #     if(request == False):
    #         check_box.click()
    # else:
    #     if(request == True):
    #         check_box.click()
    Checkbox_EMS(driver,f'ont_voip_common_echo_checkbox',request)

def Voip_Common_Profile_New_fax_mode(driver,text):
    Select(driver.find_element(By.ID,"ont_voip_common_faxmode_combobox")).select_by_visible_text(text)

def Voip_Common_Profile_New_1st_codec(driver,text):
    Select(driver.find_element(By.ID,"ont_voip_common_1stcodec_combobox")).select_by_visible_text(text)

def Voip_Common_Profile_New_2nd_codec(driver,text):
    Select(driver.find_element(By.ID,"ont_voip_common_2ndcodec_combobox")).select_by_visible_text(text)

def Voip_Common_Profile_New_3rd_codec(driver,text):
    Select(driver.find_element(By.ID,"ont_voip_common_3rdcodec_combobox")).select_by_visible_text(text)

def Voip_Common_Profile_New_4th_codec(driver,text):
    Select(driver.find_element(By.ID,"ont_voip_common_4thcodec_combobox")).select_by_visible_text(text)

def Voip_Common_Profile_New_1st_packet_period(driver,vlaue):
    input = driver.find_element(By.ID,"ont_voip_common_1st_packet_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(vlaue)

def Voip_Common_Profile_New_2nd_packet_period(driver,vlaue):
    input = driver.find_element(By.ID,"ont_voip_common_2st_packet_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(vlaue)

def Voip_Common_Profile_New_3rd_packet_period(driver,vlaue):
    input = driver.find_element(By.ID,"ont_voip_common_3st_packet_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(vlaue)

def Voip_Common_Profile_New_4th_packet_period(driver,vlaue):
    input = driver.find_element(By.ID,"ont_voip_common_4st_packet_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(vlaue)

def Voip_Common_Profile_New_1st_silence(driver,request):
    # check_box = driver.find_element(By.XPATH,'//*[@for="ont_voip_common_1st_checkbox"]')
    # if(check_box.is_selected() == True):
    #     if(request == False):
    #         check_box.click()
    # else:
    #     if(request == True):
    #         check_box.click()
    Checkbox_EMS(driver,f'ont_voip_common_1st_checkbox',request)

def Voip_Common_Profile_New_2nd_silence(driver,request):
    # check_box = driver.find_element(By.XPATH,'//*[@for="ont_voip_common_2nd_checkbox"]')
    # if(check_box.is_selected() == True):
    #     if(request == False):
    #         check_box.click()
    # else:
    #     if(request == True):
    #         check_box.click()
    Checkbox_EMS(driver,f'ont_voip_common_2nd_checkbox',request)

def Voip_Common_Profile_New_3rd_silence(driver,request):
    # check_box = driver.find_element(By.XPATH,'//*[@for="ont_voip_common_3rd_checkbox"]')
    # if(check_box.is_selected() == True):
    #     if(request == False):
    #         check_box.click()
    # else:
    #     if(request == True):
    #         check_box.click()
    Checkbox_EMS(driver,f'ont_voip_common_3rd_checkbox',request)

def Voip_Common_Profile_New_4th_silence(driver,request):
    # check_box = driver.find_element(By.XPATH,'//*[@for="ont_voip_common_4th_checkbox"]')
    # if(check_box.is_selected() == True):
    #     if(request == False):
    #         check_box.click()
    # else:
    #     if(request == True):
    #         check_box.click()
    Checkbox_EMS(driver,f'ont_voip_common_4th_checkbox',request)

def Voip_Common_Profile_New_oob_dtmf(driver,request):
    # check_box = driver.find_element(By.XPATH,'//*[@for="ont_voip_common_oob_checkbox"]')
    # if(check_box.is_selected() == True):
    #     if(request == False):
    #         check_box.click()
    # else:
    #     if(request == True):
    #         check_box.click()
    Checkbox_EMS(driver,f'ont_voip_common_oob_checkbox',request)

def Voip_Common_Profile_New_signal_code(driver,text):
    if(text == 'mul-par'):
        text = 'Multi-party'
    Select(driver.find_element(By.ID,"ont_voip_common_signal_combobox")).select_by_visible_text(text)

# # Dial Plan Profile

def Dial_Plan_Profile_New(driver):
    New_Profile(driver)

def Dial_Plan_Profile_Delete(driver):
    Delete_Profile(driver)

# def Dial_Plan_Profile_Delete_All_Select(driver,request):
#     check_box = driver.find_element(By.NAME, "rpXGSponMcastProf_chkDelall")
#     if(check_box.is_selected() == True):
#         if(request == False):
#             check_box.click()
#     else:
#         if(request == True):
#             check_box.click()

def Dial_Plan_Profile_New_Apply(driver):
    Save(driver)

# def Dial_Plan_Profile_New_Delete(driver):
#     driver.find_elements(By.CLASS_NAME, "ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-text-only")[1].click()

def Dial_Plan_Profile_New_Name(driver,name):
    Profile_Name(driver,name)

def Dial_Plan_Profile_New_MS(driver,vlaue):
    input = driver.find_element(By.ID,"ont_voip_dial_plan_maxsize_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(vlaue)

def Dial_Plan_Profile_New_CDT(driver,vlaue):
    input = driver.find_element(By.ID,"ont_voip_dial_plan_ctimeout_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(vlaue)

def Dial_Plan_Profile_New_PDT(driver,vlaue):
    input = driver.find_element(By.ID,"ont_voip_dial_plan_ptimeout_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(vlaue)
    
def Dial_Plan_Profile_New_format(driver,text):
    Select(driver.find_element(By.ID,"ont_voip_dial_plan_format_combobox")).select_by_visible_text(text)

def Dial_Plan_Profile_New_CT(driver,vlaue):
    input = driver.find_element(By.ID,"ont_voip_dial_plan_content_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(vlaue)

# ACL Profile

def ACL_Profile_New(driver):
    New_Profile(driver)

def ACL_Profile_Delete(driver):
    Delete_Profile(driver)

# def ACL_Profile_Delete_All_Select(driver,request):
#     check_box = driver.find_element(By.NAME, "rpXGSponMcastProf_chkDelall")
#     if(check_box.is_selected() == True):
#         if(request == False):
#             check_box.click()
#     else:
#         if(request == True):
#             check_box.click()

def ACL_Profile_New_Apply(driver):
    Save(driver)

# def ACL_Profile_New_Delete(driver):
#     driver.find_elements(By.CLASS_NAME, "ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-text-only")[1].click()

def ACL_Profile_New_Name(driver,name):
    Profile_Name(driver,name)

def ACL_Profile_New_Enable(driver,request):
    # check_box = driver.find_element(By.XPATH,'//*[@for="ont_acl_enable_checkbox"]')
    # if(check_box.is_selected() == True):
    #     if(request == False):
    #         check_box.click()
    # else:
    #     if(request == True):
    #         check_box.click()
    Checkbox_EMS(driver,f'ont_acl_enable_checkbox',request)

def ACL_Profile_New_Count(driver,request):
    # check_box = driver.find_element(By.XPATH,'//*[@for="ont_acl_count_checkbox"]')
    # if(check_box.is_selected() == True):
    #     if(request == False):
    #         check_box.click()
    # else:
    #     if(request == True):
    #         check_box.click()
    Checkbox_EMS(driver,f'ont_acl_count_checkbox',request)

def ACL_Profile_New_Log(driver,request):
    # check_box = driver.find_element(By.XPATH,'//*[@for="ont_acl_log_checkbox"]')
    # if(check_box.is_selected() == True):
    #     if(request == False):
    #         check_box.click()
    # else:
    #     if(request == True):
    #         check_box.click()
    Checkbox_EMS(driver,f'ont_acl_log_checkbox',request)

def ACL_Profile_New_Policy(driver,text):
    Select(driver.find_element(By.ID,"ont_acl_policy_combobox")).select_by_visible_text(text)

def ACL_Profile_New_Interface(driver,text):
    if(text == 'Lan'):
        text = 'LAN'
    elif(text == 'Wan'):
        text = 'WAN'
    Select(driver.find_element(By.ID,"ont_acl_interface_combobox")).select_by_visible_text(text)

def ACL_Profile_New_Protocol(driver,value):
    driver.find_element(By.ID,"ont_acl_protocol_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"ont_acl_protocol_text").send_keys(value)

def ACL_Profile_New_Src_Port(driver,value):
    driver.find_element(By.ID,"ont_acl_srcport_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"ont_acl_srcport_text").send_keys(value)

def ACL_Profile_New_Dst_Port(driver,value):
    driver.find_element(By.ID,"ont_acl_dstport_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"ont_acl_dstport_text").send_keys(value)

def ACL_Profile_New_Src_ip(driver,value):
    driver.find_element(By.ID,"ont_acl_srcip_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"ont_acl_srcip_text").send_keys(value)

def ACL_Profile_New_Src_mask(driver,value):
    driver.find_element(By.ID,"ont_acl_srcmask_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"ont_acl_srcmask_text").send_keys(value)

def ACL_Profile_New_Dst_ip(driver,value):
    driver.find_element(By.ID,"ont_acl_dstip_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"ont_acl_dstip_text").send_keys(value)

def ACL_Profile_New_Dst_mask(driver,value):
    driver.find_element(By.ID,"ont_acl_dstmask_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"ont_acl_dstmask_text").send_keys(value)

def ACL_Profile_New_Src_mac(driver,value):
    driver.find_element(By.ID,"ont_acl_srcmac_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"ont_acl_srcmac_text").send_keys(value)

def ACL_Profile_New_Dst_mac(driver,value):
    driver.find_element(By.ID,"ont_acl_dstmac_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"ont_acl_dstmac_text").send_keys(value)

# # ONT Alarm Profile

def Ont_Alarm_Profile_New(driver):
    New_Profile(driver)

def Ont_Alarm_Profile_Delete(driver):
    Delete_Profile(driver)

# def Ont_Alarm_Profile_Delete_All_Select(driver,request):
#     check_box = driver.find_element(By.NAME, "rpXGSponMcastProf_chkDelall")
#     if(check_box.is_selected() == True):     
#         if(request == False):
#             check_box.click()
#     else:
#         if(request == True):
#             check_box.click()

def Ont_Alarm_Profile_New_Apply(driver):
    Save(driver)
                                      
# def Ont_Alarm_Profile_New_Delete(driver):
#     driver.find_elements(By.CLASS_NAME, "ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-text-only")[1].click()

def Ont_Alarm_Profile_New_Name(driver,name):
    Profile_Name(driver,name)

def Ont_Alarm_New_Low_Current_Threshold(driver,value):
    driver.find_element(By.ID,"ont_alarm_lowC_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"ont_alarm_lowC_text").send_keys(value)

def Ont_Alarm_New_Up_Current_Threshold(driver,value):
    driver.find_element(By.ID,"ont_alarm_upC_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"ont_alarm_upC_text").send_keys(value)

def Ont_Alarm_New_Low_rxpower_thresh(driver,value):
    driver.find_element(By.ID,"ont_alarm_lowrxpower_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"ont_alarm_lowrxpower_text").send_keys(value)

def Ont_Alarm_New_Up_rxpower_thresh(driver,value):
    driver.find_element(By.ID,"ont_alarm_uprxpower_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"ont_alarm_uprxpower_text").send_keys(value)

def Ont_Alarm_New_Low_temp(driver,value):
    driver.find_element(By.ID,"ont_alarm_lowtemp_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"ont_alarm_lowtemp_text").send_keys(value)

def Ont_Alarm_New_Up_temp(driver,value):
    driver.find_element(By.ID,"ont_alarm_uptemp_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"ont_alarm_uptemp_text").send_keys(value)

def Ont_Alarm_New_Low_txpower_thresh(driver,value):
    driver.find_element(By.ID,"ont_alarm_lowtxpower_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"ont_alarm_lowtxpower_text").send_keys(value)

def Ont_Alarm_New_Up_txpower_thresh(driver,value):
    driver.find_element(By.ID,"ont_alarm_uptxpower_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"ont_alarm_uptxpower_text").send_keys(value)

def Ont_Alarm_New_Low_volt_thresh(driver,value):
    driver.find_element(By.ID,"ont_alarm_lowvolt_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"ont_alarm_lowvolt_text").send_keys(value)

def Ont_Alarm_New_Up_volt_thresh(driver,value):
    driver.find_element(By.ID,"ont_alarm_upvolt_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"ont_alarm_upvolt_text").send_keys(value)

# # XPON > Statistics 

# def Port_Statistics_Current_Statistics_Load(driver):
#     driver.find_element(By.CLASS_NAME, "font-btn").click()

# def Port_Statistics_Current_Statistics_Clear(driver):
#     driver.find_element(By.CLASS_NAME, "font-btn").click()

# #dont use xpath
# def Slot_Port_Select_Statistics(driver,text):
#     # retry = True
#     # while(retry == True):
#     #     try:
#     #         driver.find_element(By.XPATH, f"//*[@name='lctbl_selSlot']/option[{slot}]").click()
#     #     except:
#     #         time.sleep(1)
#     #     try:
#     #         if(driver.find_element(By.XPATH, f"//*[@name='lctbl_selSlot']/option[{slot}]").is_selected() == True):
#     #             retry = False
#     #     except:
#     #         time.sleep(1)

#     Select(driver.find_element(By.ID, "xgponSelOltPort")).select_by_visible_text(text)
#     # can i use this way ("Select")?

# def OntPort_Select_Statistics(driver, text):    
#     Select(driver.find_element(By.ID, "xgponSelOntPort")).select_by_visible_text(text)
#     # can i use this way ("Select")?  

# # def Port_Select(driver,port):
# #     retry = True
# #     while(retry == True):
# #         try:
# #             driver.find_element(By.XPATH, f"//*[@name='lctbl_selPort']/option[{port}]").click()
# #         except:
# #             time.sleep(1)
# #         try:
# #             if(driver.find_element(By.XPATH, f"//*[@name='lctbl_selPort']/option[{port}]").is_selected() == True):
# #                 retry = False
# #         except:
# #             time.sleep(1)

# # def Load(driver):
# #     driver.find_element(By.NAME, "lctbl_selLoad").click()


# # XPON > Diagnostic > O7 state

# def Diagnostic_Port(driver,text):    
                                      
#     Select(driver.find_element(By.ID, "rpXgponDiagnostic_IptTableOltPort")).select_by_visible_text(text)
#     # can i use this way ("Select")?

# def Diagnostic_SN(driver, value):
#     driver.find_element(By.ID, "rpXgponDiagnostic_TableSN").clear()
#     driver.find_element(By.ID, "rpXgponDiagnostic_TableSN").send_keys(value)

# # XPON > Diagnostic > Debug cmd

# def Diagnostic_Debug_cmd_system(driver, text):
#     Select(driver.find_element(By.ID, "rpXgponDiagnostic_IptTableSlot")).select_by_visible_text(text)

# def Diagnostic_Debug_cmd_port(driver, text):
#     Select(driver.find_element(By.ID, "rpXgponDiagnostic_IptTableOltPort")).select_by_visible_text(text)

# def Diagnostic_Debug_cmd_ont1(driver, text):
#     Select(driver.find_element(By.ID, "rpXgponDiagnostic_IptTableOntOltPort")).select_by_visible_text(text)

# def Diagnostic_Debug_cmd_ont2(driver, text):
#     Select(driver.find_element(By.ID, "rpXgponOntConfig_OLC3708IptTableOntPort")).select_by_visible_text(text)
                                    
# def Maintenance_Config_Reset(driver):
#     driver.switch_to.default_content()
#     driver.find_element(By.LINK_TEXT, "Maintenance").click()
#     driver.find_element(By.LINK_TEXT, "Config Reset").click()    
#     driver.switch_to.frame(0)
#     driver.find_element(By.NAME, "rpConfigReset").click()
#     pyautogui.press("enter")
#     time.sleep(60)



# EMS - Profile - IGMP Group Privilege Profile

# IGMP Group Privilege Profile                             // copy from glc

def IGMP_Privilege_Profile_Name(driver,value):
    Profile_Name(driver, value)

# def IGMP_Privilege_Profile_Index(driver,sel):
#     driver.find_element(By.XPATH, f"//*[@name='rpigmpPriProf_slt_index']/option[{sel}]").click()

def IGMP_Privilege_Profile_Active(driver,request,index):
    # check_box = driver.find_element(By.XPATH,f'//*[@for="ge_igmp_enable_checkbox{index}"]')
    # if(check_box.is_selected() == True):
    #     if(request == False):
    #         check_box.click()
    # else:
    #     if(request == True):
    #         check_box.click()
    
    Checkbox_EMS(driver,'ge_igmp_enable_checkbox',request,index)

def IGMP_Privilege_Profile_Bandwidth(driver,value,index):
    input = driver.find_element(By.ID,f"ge_igmp_bandwidth_text{index}")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(value)

def IGMP_Privilege_Profile_Start_Address(driver,value,index):
    input = driver.find_element(By.ID,f"ge_igmp_startip_text{index}")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(value)

def IGMP_Privilege_Profile_End_Address(driver,value,index):
    input = driver.find_element(By.ID,f"ge_igmp_endip_text{index}")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(value)

def IGMP_Privilege_Profile_Privilege(driver,text,index):
    Select(driver.find_element(By.ID,f"ge_igmp_privilege_combobox{index}")).select_by_visible_text(text)  

def IGMP_Privilege_Profile_Length(driver,value,index):
    input = driver.find_element(By.ID,f"ge_igmp_preview_length_text{index}")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(value)

def IGMP_Privilege_Profile_Interval(driver,value,index):
    input = driver.find_element(By.ID,f"ge_igmp_preview_interval_text{index}")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(value)

def IGMP_Privilege_Profile_Count(driver,value,index):
    input = driver.find_element(By.ID,f"ge_igmp_preview_count_text{index}")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(value)

def IGMP_Privilege_Profile_Reset(driver,value,index):
    input = driver.find_element(By.ID,f"ge_igmp_preview_reset_text{index}")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(value)

def IGMP_Privilege_Profile_Apply_New(driver):
    # driver.find_element(By.ID,"rpigmpPriProf_config_button_apply").click()
    Save(driver)

# def IGMP_Privilege_Profile_Delete_Entry(driver):
#     driver.find_element(By.ID,"rpigmpPriProf_config_button_cancel").click()

# def IGMP_Privilege_Profile_Modify(driver):
#     driver.find_element(By.ID,"rpigmpPriProf_data_button_modify").click()

# def IGMP_Privilege_Profile_Delete(driver):
#     driver.find_element(By.ID,"rpigmpPriProf_data_button_delete").click()


# EMS - Profile - Shaping
#  > Shaping

def Shaping_Profile_Name(driver,value):
    Profile_Name(driver,value)

def Shaping_Max_Rate_Queue(driver,Queue,value):
    input = driver.find_element(By.ID,f"ge_shaping_queue{Queue}_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(value)

def Shaping_Apply(driver):
    Save(driver)

# def Shaping_Delete(driver):
#     driver.find_element(By.NAME, "rpprofqosshape_btnDelete").click()


# EMS - Profile - Weight
# > Weight

def Weight_Profile_Name(driver,value):
    Profile_Name(driver,value)

def Weight_Weight_Queue(driver,Queue,value):
    input = driver.find_element(By.ID,f"ge_weight_queue{Queue}_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(value)

def Weight_Apply(driver):
    Save(driver)

# def Weight_Delete(driver):
#     driver.find_element(By.NAME, "rpprofqoswrr_btnDelete").click()


# EMS - Profile - Rate Limit
# > RateLimit

def RateLimit_Profile_Name(driver,value):
    Profile_Name(driver,value)

def RateLimit_Ingress_Checkbox(driver, request):
    # check_box = driver.find_element(By.XPATH,f'//*[@for="ge_ratelimit_ingress_checkbox"]')
    # if(check_box.is_selected() == True):
    #     if(request == False):
    #         check_box.click()
    # else:
    #     if(request == True):
    #         check_box.click()
    Checkbox_EMS(driver,'ge_ratelimit_ingress_checkbox',request)

def RateLimit_Ingress_CIR(driver,CIR):
    input = driver.find_element(By.ID,f"ge_ratelimit_ingress_cir_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(CIR)

def RateLimit_Ingress_CBS(driver,CBS):
    input = driver.find_element(By.ID,f"ge_ratelimit_ingress_cbs_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(CBS)

def RateLimit_Ingress_EIR(driver,EIR):
    input = driver.find_element(By.ID,f"ge_ratelimit_ingress_eir_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(EIR)

def RateLimit_Ingress_EBS(driver,EBS):
    input = driver.find_element(By.ID,f"ge_ratelimit_ingress_ebs_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(EBS)

def RateLimit_Ingress(driver,request,CIR,CBS,EIR,EBS):
    RateLimit_Ingress_Checkbox(driver, request)
    RateLimit_Ingress_CIR(driver,CIR)
    RateLimit_Ingress_CBS(driver,CBS)
    RateLimit_Ingress_EIR(driver,EIR)
    RateLimit_Ingress_EBS(driver,EBS)

def RateLimit_Egress_Checkbox(driver,request):
    # check_box = driver.find_element(By.XPATH,f'//*[@for="ge_ratelimit_egress_checkbox"]')
    # if(check_box.is_selected() == True):
    #     if(request == False):
    #         check_box.click()
    # else:
    #     if(request == True):
    #         check_box.click()
    Checkbox_EMS(driver,'ge_ratelimit_egress_checkbox',request)

def RateLimit_Egress_RATE(driver,Rate):
    input = driver.find_element(By.ID,f"ge_ratelimit_egress_rate_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(Rate)

def RateLimit_Egress_BURST(driver,Burst):
    input = driver.find_element(By.ID,f"ge_ratelimit_egress_burst_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(Burst)

def RateLimit_Egress(driver,request,Rate,Burst):
    RateLimit_Egress_Checkbox(driver,request)
    RateLimit_Egress_RATE(driver,Rate)
    RateLimit_Egress_BURST(driver,Burst)

def RateLimit_Apply(driver):
    Save(driver)

# def RateLimit_Delete(driver):
#     driver.find_element(By.NAME, "rpprofqosrlp_btnDelete").click()


# GE Template

def GE_Template_Profile_Name(driver,value):
    Profile_Name(driver,value)

def GE_Template_Apply(driver):
    Save(driver)

def GE_Template_Auto_Nego(driver,request):
    # check_box = driver.find_element(By.XPATH,f'//*[@for="ge_template_autonego_checkbox"]')
    # if(check_box.is_selected() == True):        
    #     if(request == False):
    #         check_box.click()
    # else:
    #     if(request == True):
    #         check_box.click()
    Checkbox_EMS(driver,'ge_template_autonego_checkbox',request)

def GE_Template_Flow_Ctrl(driver,request):
    # check_box = driver.find_element(By.XPATH,f'//*[@for="ge_template_flowctrl_checkbox"]')
    # if(check_box.is_selected() == True):        
    #     if(request == False):
    #         check_box.click()
    # else:
    #     if(request == True):
    #         check_box.click()
    Checkbox_EMS(driver,'ge_template_flowctrl_checkbox',request)

def GE_Template_Speed(driver,text):
    Select(driver.find_elements(By.ID,f"ge_template_speed_combobox")[0]).select_by_visible_text(text) 

def GE_Template_MTU(driver,text):
    input = driver.find_element(By.ID,f"ge_template_mtu_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(text)

def GE_Template_VLAN_Untag_And_Copy_Cpbit_PVID(driver,text):
    input = driver.find_element(By.ID,f"ge_template_pvid_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(text)

def GE_Template_VLAN_Untag_And_Copy_Cpbit_Pbit(driver,text):
    input = driver.find_element(By.ID,f"ge_template_pbit_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(text)

def GE_Template_VLAN_Untag_And_Copy_Cpbit_Frame_Type(driver,text):
    Select(driver.find_elements(By.ID,f"ge_template_speed_combobox")[1]).select_by_visible_text(text) 

def GE_Template_VLAN_Untag_And_Copy_Cpbit_Copy_Cpbit(driver,request):
    # check_box = driver.find_element(By.XPATH,f'//*[@for="ge_template_copycpbit_checkbox"]')
    # if(check_box.is_selected() == True):        
    #     if(request == False):
    #         check_box.click()
    # else:
    #     if(request == True):
    #         check_box.click()
    Checkbox_EMS(driver,'ge_template_copycpbit_checkbox',request)

def GE_Template_VLAN_Untag_And_Copy_Cpbit_Outer_TPID(driver,request):
    # check_box = driver.find_element(By.XPATH,f'//*[@for="ge_template_outertpid_checkbox"]')
    # if(check_box.is_selected() == True):        
    #     if(request == False):
    #         check_box.click()
    # else:
    #     if(request == True):
    #         check_box.click()
    Checkbox_EMS(driver,'ge_template_outertpid_checkbox',request)
# VLAN
def GE_Template_VLAN_New(driver):
    driver.find_element(By.ID,'ge_template_vlantable_vlan_add').click()

def GE_Template_VLAN_New_VLAN_ID(driver,text):
    input = driver.find_element(By.ID,f"ge_template_vid_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(text)

def GE_Template_VLAN_New_Mode(driver,text):
    Select(driver.find_element(By.ID,f"ge_template_mode_combobox")).select_by_visible_text(text) 

def GE_Template_VLAN_New_Untag(driver,request):
    # check_box = driver.find_element(By.XPATH,f'//*[@for="ge_template_untag_checkbox"]')
    # if(check_box.is_selected() == True):        
    #     if(request == False):
    #         check_box.click()
    # else:
    #     if(request == True):
    #         check_box.click()
    Checkbox_EMS(driver,'ge_template_untag_checkbox',request)

def GE_Template_VLAN_New_OK(driver):
    driver.find_element(By.ID,'popupCallBack').click()

def GE_Template_VLAN_New_Select(driver,index):
    Checkbox_EMS(driver,f'ge_template_vlan_del_checkbox{index}',True)

def GE_Template_VLAN_Delete(driver):
    driver.find_element(By.ID,'ge_template_vlantable_vlan_delete').click()
# VLAN TLS
def GE_Template_VLAN_TLS_New(driver):
    driver.find_element(By.ID,'ge_template_vlantable_vlantls_add').click()

def GE_Template_VLAN_TLS_Select(driver,index):
    Checkbox_EMS(driver,f'ge_template_vlantls_del_checkbox{index}',True)

def GE_Template_VLAN_TLS_Delete(driver):
    driver.find_element(By.ID,'ge_template_vlantable_vlantls_delete').click()

def GE_Template_VLAN_TLS_New_SVID(driver,text):
    input = driver.find_element(By.ID,f"ge_template_tlssvid_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(text)

def GE_Template_VLAN_TLS_New_Spbit(driver,text):
    input = driver.find_element(By.ID,f"ge_template_tlsspbit_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(text)

def GE_Template_VLAN_TLS_New_OK(driver):
    driver.find_element(By.ID,'popupCallBack').click()

def GE_Template_VLAN_TLS_Delete(driver):
    driver.find_element(By.ID,'ge_template_vlantable_vlantls_delete').click()

# VLAN Trunk : Uni-UnTag
def GE_Template_VLAN_Trunk_Uni_UnTag_New(driver):
    driver.find_element(By.ID,'ge_template_vlantable_untag_add').click()

def GE_Template_VLAN_Trunk_Uni_UnTag_Select(driver,index):
    Checkbox_EMS(driver,f'ge_template_uni_untag_del_checkbox{str(index)}',True)

def GE_Template_VLAN_Trunk_Uni_UnTag_Delete(driver):
    driver.find_element(By.ID,'ge_template_vlantable_untag_delete').click()

# VLAN Trunk : UNI Untag For Ether Type
def GE_Template_VLAN_Trunk_Uni_UnTag_EtherType_New(driver):
    driver.find_element(By.ID,'ge_template_vlantable_untag_ether_add').click()

def GE_Template_VLAN_Trunk_Uni_UnTag_EtherType_Select(driver,index):
    Checkbox_EMS(driver,f'ge_template_uni_untag_ether_del_checkbox{index}',True)

def GE_Template_VLAN_Trunk_Uni_UnTag_EtherType_Delete(driver):
    driver.find_element(By.ID,'ge_template_vlantable_untag_ether_delete').click()

def GE_Template_VLAN_Trunk_Uni_UnTag_EtherType_New_SVID(driver,text):
    input = driver.find_element(By.ID,f"ge_template_svid_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(text)

def GE_Template_VLAN_Trunk_Uni_UnTag_EtherType_New_SPbit(driver,text):
    input = driver.find_element(By.ID,f"ge_template_spbit_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(text)

def GE_Template_VLAN_Trunk_Uni_UnTag_EtherType_New_OK(driver):
    OK(driver)

def GE_Template_VLAN_Trunk_Uni_UnTag_New_Ether_Type(driver,text):    
    request = True
    # check_box = driver.find_element(By.XPATH,f'//*[@for="ge_template_ethertype_checkbox"]')
    # if(check_box.is_selected() == True):        
    #     if(request == False):
    #         check_box.click()
    # else:
    #     if(request == True):
    #         check_box.click()
    # Checkbox_EMS(driver,'ge_template_ethertype_checkbox',request)
    input = driver.find_element(By.ID,f"ge_template_ethertype_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(text)

def GE_Template_VLAN_Trunk_Uni_UnTag_New_Subnet_IP(driver,text):    
    request = True
    # check_box = driver.find_element(By.XPATH,f'//*[@for="ge_template_subnet_checkbox"]')
    # if(check_box.is_selected() == True):        
    #     if(request == False):
    #         check_box.click()
    # else:
    #     if(request == True):
    #         check_box.click()
    Checkbox_EMS(driver,'ge_template_subnet_checkbox',request)
    input = driver.find_element(By.ID,f"ge_template_address_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(text)

def GE_Template_VLAN_Trunk_Uni_UnTag_New_SVID(driver,text):
    input = driver.find_element(By.ID,f"ge_template_svid_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(text)

def GE_Template_VLAN_Trunk_Uni_UnTag_New_CVID(driver,text):
    input = driver.find_element(By.ID,f"ge_template_cvid_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(text)

def GE_Template_VLAN_Trunk_Uni_UnTag_New_Spbit(driver,text):
    input = driver.find_element(By.ID,f"ge_template_spbit_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(text)

def GE_Template_VLAN_Trunk_Uni_UnTag_New_OK(driver):
    driver.find_element(By.ID,'popupCallBack').click()

def GE_Template_VLAN_Trunk_Uni_UnTag_Delete(driver):
    driver.find_element(By.ID,'ge_template_vlantable_untag_delete').click()
# VLAN Trunk : UNI-VLAN
def GE_Template_VLAN_Trunk_UNI_VLAN_New(driver):
    driver.find_element(By.ID,'ge_template_vlantable_univlan_add').click()

def GE_Template_VLAN_Trunk_UNI_VLAN_Select(driver,index):
    Checkbox_EMS(driver,f'ge_template_univlan_del_checkbox{index}',True)

def GE_Template_VLAN_Trunk_UNI_VLAN_Delete(driver):
    driver.find_element(By.ID,'ge_template_vlantable_univlan_delete').click()

def GE_Template_VLAN_Trunk_UNI_VLAN_New_Uni_VID(driver,text):    
    input = driver.find_elements(By.ID,f"ge_template_uniuntag_text")[0]
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(str(text))

def GE_Template_VLAN_Trunk_UNI_VLAN_New_SVID(driver,text):    
    input = driver.find_elements(By.ID,f"ge_template_uniuntag_text")[1]                # id 重複
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(str(text))

def GE_Template_VLAN_Trunk_UNI_VLAN_New_OK(driver):
    driver.find_element(By.ID,'popupCallBack').click()

def GE_Template_VLAN_Trunk_UNI_VLAN_Delete(driver):
    driver.find_element(By.ID,'ge_template_vlantable_univlan_delete').click()
# VLAN Translation
def GE_Template_VLAN_Translation_New(driver):
    driver.find_element(By.ID,'ge_template_vlantable_trans_add').click()

def GE_Template_VLAN_Translation_Select(driver,index):
    Checkbox_EMS(driver,f'ge_template_trans_del_checkbox{index}',True)

def GE_Template_VLAN_Translation_Delete(driver):
    driver.find_element(By.ID,'ge_template_vlantable_trans_delete').click()

def GE_Template_VLAN_Translation_New_Mode(driver,text):
    if(text == 'Single-SVlan'):
        text = 'Single SVLAN'
    elif(text == 'Double-Vlan'):
        text = 'Double VLAN'
    elif(text == 'Uni-Vlan'):
        text = 'Uni VLAN'
    Select(driver.find_element(By.ID,f"ge_template_transmode_combobox")).select_by_visible_text(text) 

def GE_Template_VLAN_Translation_New_Uni_VID(driver,text):    
    input = driver.find_element(By.ID,f"ge_template_univid_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(text)

def GE_Template_VLAN_Translation_New_SVID(driver,text):    
    input = driver.find_element(By.ID,f"ge_template_transsvid_text")         
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(text)

def GE_Template_VLAN_Translation_New_Spbit(driver,text):    
    input = driver.find_element(By.ID,f"ge_template_transspbit_text")         
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(text)

def GE_Template_VLAN_Translation_New_CTag_Add(driver,request):
    Checkbox_EMS(driver,'ge_template_ctag_checkbox',request)

def GE_Template_VLAN_Translation_New_CVID(driver,text):    
    request = True
    # check_box = driver.find_element(By.XPATH,f'//*[@for="ge_template_ctag_checkbox"]')
    # if(check_box.is_selected() == True):        
    #     if(request == False):
    #         check_box.click()
    # else:
    #     if(request == True):
    #         check_box.click()
    Checkbox_EMS(driver,'ge_template_ctag_checkbox',request)
    input = driver.find_element(By.ID,f"ge_template_transcvid_text")         
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(text)

def GE_Template_VLAN_Translation_New_OK(driver):
    driver.find_element(By.ID,'popupCallBack').click()

def GE_Template_VLAN_Translation_Delete(driver):
    driver.find_element(By.ID,'ge_template_vlantable_trans_delete').click()
# IGMP Group Privilege Profile
def GE_Template_IGMP_Group_Privilege_Profile_Max_Group(driver,text):
    input = driver.find_element(By.ID,f"ge_template_maxgroup_text")         
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(text)

def GE_Template_IGMP_Group_Privilege_Profile_Max_Message(driver,text):
    input = driver.find_element(By.ID,f"ge_template_maxmessage_text")         
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(text)

def GE_Template_IGMP_Group_Privilege_Profile_Group_Privilege(driver,request):
    # check_box = driver.find_element(By.XPATH,f'//*[@for="ge_template_groupenable_checkbox"]')
    # if(check_box.is_selected() == True):        
    #     if(request == False):
    #         check_box.click()
    # else:
    #     if(request == True):
    #         check_box.click()
    Checkbox_EMS(driver,'ge_template_groupenable_checkbox',request)

def GE_Template_IGMP_Group_Privilege_Profile_Profile(driver,text):
    Select(driver.find_element(By.ID,f"ge_template_igmp_combobox")).select_by_visible_text(text) 

def GE_Template_IGMP_Group_Privilege_Profile_Profile_Deselect_all(driver):
    Select(driver.find_element(By.ID,f"ge_template_igmp_combobox")).deselect_all()

# QOS Setup
def GE_Template_QOS_Setup_Algorithm(driver,text):
    Select(driver.find_element(By.ID,f"ge_template_algor_combobox")).select_by_visible_text(text) 

def GE_Template_QOS_Setup_Rate_Limit_Profile(driver,text):
    Select(driver.find_element(By.ID,f"ge_template_ratelimit_combobox")).select_by_visible_text(text) 

def GE_Template_QOS_Setup_Shaping_Profile(driver,text):
    Select(driver.find_element(By.ID,f"ge_template_shaping_combobox")).select_by_visible_text(text) 

def GE_Template_QOS_Setup_Weight_Profile(driver,text):
    Select(driver.find_element(By.ID,f"ge_template_weight_combobox")).select_by_visible_text(text) 






