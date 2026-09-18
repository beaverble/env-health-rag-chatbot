from datetime import datetime
import re


def make_card_prompt(env_df, outdoor_df, user_height, user_weight, user_pressure, user_suger, user_systolic, user_diastolic, user_bloodSugar):
    with open('prompt/system.txt', 'r', encoding='utf-8') as file:
        system_prompt = file.read()

    pattern_001 = r'#001'
    pattern_002 = r'#002'
    pattern_003 = r'#003'
    pattern_004 = r'#004'
    pattern_005 = r'#005'
    pattern_006 = r'#006'
    pattern_007 = r'#007'
    pattern_008 = r'#008'
    pattern_009 = r'#009'

    pattern_101 = r'#101'
    pattern_102 = r'#102'
    pattern_103 = r'#103'
    pattern_104 = r'#104'
    pattern_105 = r'#105'
    pattern_106 = r'#106'
    pattern_107 = r'#107'
    pattern_108 = r'#108'
    pattern_109 = r'#109'
    pattern_110 = r'#110'
    pattern_111 = r'#111'

    pattern_201 = r'#201'
    pattern_202 = r'#202'
    pattern_203 = r'#203'
    pattern_204 = r'#204'
    pattern_205 = r'#205'
    pattern_206 = r'#206'

    # 치환: 패턴에 맞는 위치를 찾아서 값을 Series에서 가져옴
    with open('./prompt/user.txt', 'r', encoding='utf-8') as file:
        user_prompt = file.read()
    if user_height is not None and user_weight is not None and env_df is not None:
        if 250 > float(user_height) > 50:
            user_prompt = re.sub(pattern_001, f'{user_height}cm', user_prompt)
        if 200 > float(user_weight) > 20:
            user_prompt = re.sub(pattern_002, f'{user_weight}kg', user_prompt)
        if env_df["APLY_GENDER"] == 'M':
            user_prompt = re.sub(pattern_003, '남성', user_prompt)
            if float(user_height) <= 50 or float(user_height) >= 250:
                user_prompt = re.sub(pattern_001, f'{171.49}cm', user_prompt)
            if float(user_weight) <= 20 or float(user_weight) >= 200:
                user_prompt = re.sub(pattern_002, f'{74.33}kg', user_prompt)
        else:
            user_prompt = re.sub(pattern_003, '여성', user_prompt)
            if float(user_height) <= 50 or float(user_height) >= 250:
                user_prompt = re.sub(pattern_001, f'{158.26}cm', user_prompt)
            if float(user_weight) <= 20 or float(user_weight) >= 200:
                user_prompt = re.sub(pattern_002, f'{58.65}kg', user_prompt)
        user_prompt = re.sub(pattern_004, f'{env_df["APLY_AGE"]}세', user_prompt)
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        user_prompt = re.sub(pattern_005, f'{now_time}', user_prompt)
        system_prompt = system_prompt + "\n"+ user_prompt
    else:
        system_prompt = system_prompt + "\n[현재 시각] " + datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        user_prompt = '[사용자 정보]\n없음'

    with open('./prompt/health.txt', 'r', encoding='utf-8') as file:
        health_prompt = file.read()
    if user_systolic is not None and user_diastolic is not None and user_bloodSugar is not None:
        health_prompt = re.sub(pattern_007, f'{user_systolic}', health_prompt)
        system_prompt = system_prompt + health_prompt
        health_prompt = re.sub(pattern_008, f'{user_diastolic}', health_prompt)
        system_prompt = system_prompt + health_prompt
        health_prompt = re.sub(pattern_009, f'{user_bloodSugar}', health_prompt)
        system_prompt = system_prompt + "\n"+ health_prompt
    else:
        health_prompt = '[건강 정보]\n없음'

    with open('./prompt/disease.txt', 'r', encoding='utf-8') as file:
        disease_prompt = file.read()
    if user_pressure is not None and user_suger is not None:
        if user_pressure == 'Y':
            if user_suger == 'Y':
                user_disease = '고혈압, 당뇨'
            else:
                user_disease = '고혈압'
        else:
            if user_suger == 'Y':
                user_disease = '당뇨'
            else:
                user_disease = '없음'
        disease_prompt = re.sub(pattern_006, f'{user_disease}', disease_prompt)
        system_prompt = system_prompt + "\n"+ disease_prompt
    else:
        disease_prompt = '[건강정보 정보]\n없음'

    with open('./prompt/indoor.txt', 'r', encoding='utf-8') as file:
        indoor_prompt = file.read()
    if env_df is not None:
        if 's00' in env_df:
            indoor_prompt = re.sub(pattern_101, f'{env_df["s00"]}µg/m³', indoor_prompt)
            indoor_prompt = re.sub(pattern_102, f'{env_df["s01"]}µg/m³', indoor_prompt)
            indoor_prompt = re.sub(pattern_103, f'{env_df["s02"]}µg/m³', indoor_prompt)
            indoor_prompt = re.sub(pattern_104, f'{env_df["s03"]}µg/m³', indoor_prompt)
            indoor_prompt = re.sub(pattern_105, f'{env_df["s04"]}ppm', indoor_prompt)
            indoor_prompt = re.sub(pattern_106, f'{env_df["s05"]}도', indoor_prompt)
            indoor_prompt = re.sub(pattern_107, f'{env_df["s06"]}%', indoor_prompt)
            indoor_prompt = re.sub(pattern_108, f'{env_df["s09"]}ppm', indoor_prompt)
            indoor_prompt = re.sub(pattern_109, f'{env_df["s011"]}ppm', indoor_prompt)
            indoor_prompt = re.sub(pattern_110, f'{env_df["s012"]}ppm', indoor_prompt)
            indoor_prompt = re.sub(pattern_111, f'{env_df["s013"]}ppm', indoor_prompt)
        else:
            indoor_prompt = '[실내 환경 정보]\n없음'
        system_prompt = system_prompt + "\n"+ indoor_prompt
    else:
        indoor_prompt = '[실내 환경 정보]\n없음'

    if outdoor_df is None:
        outdoor_prompt = '[실외 환경 정보]\n없음'
    else:
        with open('./prompt/outdoor.txt', 'r', encoding='utf-8') as file:
            outdoor_prompt = file.read()
        outdoor_prompt = re.sub(pattern_201, f'{outdoor_df["o3"]}ppm', outdoor_prompt)
        outdoor_prompt = re.sub(pattern_202, f'{outdoor_df["no2"]}ppm', outdoor_prompt)
        outdoor_prompt = re.sub(pattern_203, f'{outdoor_df["co"]}ppm', outdoor_prompt)
        outdoor_prompt = re.sub(pattern_204, f'{outdoor_df["so2"]}ppm', outdoor_prompt)
        outdoor_prompt = re.sub(pattern_205, f'{outdoor_df["pm25"]}µg/m³', outdoor_prompt)
        outdoor_prompt = re.sub(pattern_206, f'{outdoor_df["pm10"]}µg/m³', outdoor_prompt)
        system_prompt = system_prompt + "\n"+ outdoor_prompt

    return system_prompt, user_prompt, health_prompt, disease_prompt, indoor_prompt, outdoor_prompt
