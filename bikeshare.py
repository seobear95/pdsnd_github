# -*- coding: utf-8 -*-
import time
import pandas as pd
import numpy as np

#from google.colab import drive
#drive.mount('/content/drive')

"""CITY_DATA, MONTHS, DAYS
CITY_DATA: 세 도시의 데이터 파일 이름을 저장하는 딕셔너리입니다. 각 도시 이름이 키(key)이고, 해당 CSV 파일의 이름이 값(value)입니다.

MONTHS: 분석할 수 있는 월(month)의 목록입니다. 'all' 옵션은 모든 월을 포함합니다.


DAYS: 분석할 수 있는 요일(day)의 목록입니다. 'All' 옵션은 모든 요일을 포함합니다.
"""

"""CITY_DATA = {
    'chicago': '/content/drive/My Drive/chicago.csv',
    'new york city': '/content/drive/My Drive/new_york_city.csv',
    'washington': '/content/drive/My Drive/washington.csv'
}"""

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

# Add months of the year
# 1월, 2월, 3월, 4월, 5월, 6월, 모든 월 을 리스트 항목으로 가지는 MONTHS 리스트객체 
MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'all']


# Add days of the week
# 월요일, 화요일, 수요일, 목요일, 금요일, 토요일, 일요일, 모든요일을 항목으로 가지는 DAYS 리스트 객체
DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'All']

"""get_filters()
사용자에게 도시, 월, 요일을 입력받아 분석할 데이터의 필터를 설정합니다.

입력받은 값들은 소문자 또는 타이틀 케이스로 변환되어 올바른 형식으로 처리됩니다.

잘못된 입력을 방지하기 위해 while 루프를 사용하여 사용자가 유효한 값을 입력할 때까지 반복 요청합니다.
"""

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Please choose a city >>> (Chicago, New York City or Washington): ").lower()
    # Prevent error if incorrect
    while city not in CITY_DATA:
        print("Please try again, name not recognized")
        city = input("Please choose a city >>> (Chicago, New York City or Washington): ").lower()

    # TO DO: get user input for month (all, january, february, ... , june)
    month = input("Please choose a month >>> (January, February, March, April, May, June or All): ").lower()
    # Prevent error if incorrect
    while month not in MONTHS:
        print("Please try again, month not recognized")
        month = input("Please choose a month >>> (January, February, March, April, May, June or All): ").lower()

     # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Please choose a Day >>> (Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or All): ").title()
    # Prevent error if incorrect
    while day not in DAYS:
        print("Please try again, day not recognized")
        day = input("Please choose a day >>> (Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or All): ").title()

    print('-'*40)
    return city, month, day

"""데이터 로딩 및 전처리

load_data(city, month, day)

선택된 도시의 데이터를 CSV 파일에서 읽어와 판다스 데이터프레임으로 변환합니다.

데이터를 정리하고, 필요한 새로운 열(예: 월, 요일)을 추가합니다.
사용자가 선택한 월과 요일에 따라 데이터를 필터링합니다.
"""

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    #Read and load in as df to return df / use CITY DATA
    df = pd.read_csv(CITY_DATA[city])

    # Clean Data
    #Columns unnamed = 0  drop
    df.drop(columns='Unnamed: 0', inplace=True)

    #Missing values
    df.fillna(method='ffill', inplace=True)

    # Change data types
    # Change startime/ endtime to datetime format
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # convert 'End Time' column to datetime.
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month from 'Start Time' column to create 'Month' column.
    df['Month'] = df['Start Time'].dt.month

    # extract day from 'Start Time' column to create 'Day' column.
    df['Day'] = df['Start Time'].dt.day_name()

    # filter by month
    if month != 'all':
        month_index = MONTHS.index(month) + 1
        df = df[df['Month'] == month_index]

    # Filter by day
    if day != 'All':
        df = df[df['Day'] == day]

    return df

"""

통계 분석 함수들
time_stats(df, month, day)
가장 흔한 여행 월, 요일, 시간을 계산합니다.
# 코드로 형식 지정됨


"""

def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # # TO DO: display the most common month
    if month == 'all':

        print('The most common month is: ', MONTHS[df['Month'].mode()[0] - 1].title() )
    else:

        print('The most common month is: ', month.title())

    # TO DO: display the most common day of week
    if day == 'All':

        print('The most common day is: ', df['Day'].mode()[0])
    else:

        print('The most common day is: ', day)


    # TO DO: display the most common start hour
    # First need to create columns for start time and start hour to find common start hour
    df['Start Hour'] = df['Start Time'].dt.hour

    # TO DO: display the most common start hour
    print('The Most Common Start Hour is: ', df['Start Hour'].mode()[0])


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

"""station_stats(df)
가장 인기 있는 출발역과 도착역, 그리고 여행 경로를 계산합니다.
데이터프레임을 통해 자전거 공유 서비스의 인기 있는 출발역, 도착역, 그리고 여행 경로에 대한 통계를 제공합니다. 이를 통해 사용자는 서비스의 이용 패턴을 더 잘 이해할 수 있습니다.

trip_duration_stats(df)
총 여행 시간과 평균 여행 시간을 계산합니다.
자전거 공유 데이터에서 여행의 총 시간과 평균 시간을 계산하는 기능을 합니다. 이 함수는 판다스 데이터프레임 df를 입력으로 받아, 해당 데이터프레임에서 여행 시간과 관련된 통계를 계산

user_stats(df)
사용자 유형, 성별, 출생 연도에 대한 통계를 제공합니다.자전거 공유 데이터에서 사용자 관련 통계를 계산하고 출력하는 역할을 합니다. 이 함수는 판다스 데이터프레임 df를 입력으로 받아, 해당 데이터프레임에서 다양한 사용자 통계를 계산합니다.

원시 데이터 표시
raw_data(df)
사용자가 원할 경우, 데이터의 원시 행을 5개씩 표시합니다.데이터프레임 df에서 원시 데이터(raw data)의 일부를 보여주는 기능을 합니다. 이 함수는 사용자에게 원시 데이터를 보고 싶은지 묻고, 'yes'라고 대답하면 데이터프레임의 일부를 출력합니다. 사용자가 더 이상 데이터를 보고 싶지 않을 때까지 이 과정을 반복
"""

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print('The Most Commonly used Start Station is: ' , df['Start Station'].mode()[0])

     # TO DO: display most commonly used end station
    print('The Most Commonly used End Station is: ' , df['End Station'].mode()[0])

    #이 함수는 df라는 이름의 데이터프레임을 매개변수로 받습니다.
    # 이 데이터프레임에는 자전거 공유 서비스의 여행 데이터가 들어 있습니다.
    # df['Start Station']은 모든 여행의 출발역을 나타내는 열
    # mode()[0] 메소드는 이 열에서 가장 자주 나타나는 값을 찾습니다. 즉, 가장 인기 있는 출발역을 찾는 데 사용
    #df['End Station']은 모든 여행의 도착역을 나타내는 열입니다.
    # .mode()[0] 메소드를 사용하여 가장 자주 나타나는 도착역, 즉 가장 인기 있는 도착역을 찾습니다.
    #  데이터프레임이나 시리즈에서 가장 자주 나타나는 값을 찾는 데 사용. '최빈값(mode)'이라고 합니다.
    # 여기서 .mode() 함수는 최빈값을 찾고, [0]은 그 중 첫 번째 값을 선택합니다.

   # TO DO: display most frequent combination of start station and end station
    df['journey'] = df['Start Station'] + " to " + df['End Station']
    print('The Most Frequent Trip from: ', df['journey'].mode()[0])

#df['Start Station']과 df['End Station']을 결합하여 각 여행의 출발역과 도착역을 나타내는 새로운 열 df['journey']를 만듭니다.
# .mode()[0] 메소드를 사용하여 가장 자주 나타나는 여행 경로, 즉 가장 인기 있는 여행 경로를 찾습니다.
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #sum() 메소드는 이 열의 모든 값을 합산합니다.
    # 즉, 데이터셋에 있는 모든 여행의 총 지속 시간을 계산합니다.
    # 결과는 초 단위로 출력
    # TO DO: display total travel time / sum = total
    print('The Total Travel Time is: ', df['Trip Duration'].sum(), "'sec")


#mean() 메소드는 이 열의 평균 값을 계산합니다.
#즉, 모든 여행의 평균 지속 시간을 찾습니다.
#결과는 정수로 변환되어 초 단위로 출력
    # TO DO: display mean travel time / mean = average
    print('The Mean Travel Time is: ', int(df['Trip Duration'].mean()), "'sec")

#함수의 실행 시간을 계산하고 출력
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

#df['User Type']은 각 여행을 한 사용자의 유형(예: 일반 사용자, 구독자 등)을 나타내는 열
#value_counts() 메소드는 이 열의 각 값(사용자 유형)이 몇 번 나타나는지 계산합니다. 즉, 각 사용자 유형의 빈도수

    user_type = df['User Type'].value_counts()

    print(f"The types of users by number are given below:\n\n{user_type}")

    #Missing data for gender and birth year need to prevent error if user selects this filter
#df['Gender'] 열은 사용자의 성별을 나타냅니다.
#value_counts() 메소드를 사용하여 각 성별의 빈도수를 계산합니다.
#try-except 블록은 'Gender' 열이 데이터에 없는 경우(예: 데이터셋에 성별 데이터가 포함되지 않은 경우)를 처리합니다.
#성별 데이터가 없으면, 적절한 메시지를 출력

    try:
        gender = df['Gender'].value_counts()
        print(f"\nThe types of users by gender is available:\n\n{gender}")
    except:
        print("\nThere is no 'Gender' data in this file.")

    # TO DO: Display earliest, most recent, and most common year of birth / earliest = min, recent = max, common = mode
   #min(), max(), mode()[0] 메소드를 사용하여 가장 이른, 가장 최근, 그리고 가장 흔한 출생 연도
    try:
        earliest = int(df['Birth Year'].min())
        recent = int(df['Birth Year'].max())
        common_year = int(df['Birth Year'].mode()[0])
        print(f"\nThe earliest year of birth: {earliest}\n\nThe most recent year of birth: {recent}\n\nThe most common year of birth: {common_year}")
    except:
        print("There are no birth year data in this file.")

    print("\This took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(df):
    """ Displays 5 lines of raw data at a time when yes is selected."""
    # Create index and increase by 5
    #i는 데이터프레임에서 보여줄 행의 시작 인덱스를 나타냅니다. 초기값은 1로 설정
    i = 1

    #while True 루프는 사용자가 'no'라고 입력할 때까지 계속 실행됩니다.
    #input() 함수를 사용하여 사용자에게 데이터를 더 볼지 묻습니다.
    #사용자가 'yes'라고 대답하면, df[i:i+5]를 통해 데이터프레임의 i번째 행부터 i+4번째 행까지 총 5행을 출력합니다.
    #그 후 i의 값을 5 증가시켜 다음 번에 다음 5행을 보여줄 수 있도록 합니다.
    #사용자가 'yes'가 아닌 다른 것을 입력하면, break 문을 통해 루프를 종료합니다

    while True:
        rawdata = input('\nWould you like to see 5 lines of raw data? Enter yes or no.\n')
        if rawdata.lower() == 'yes':
            # print 5 lines
            print(df[i:i+5])

            # increase index by 5
            i = i+5

        else:
            # prevent errors
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes to continue: ')
        if restart.lower() not in ['yes', 'y'] :
            break


if __name__ == "__main__":
	main()

"""메인 함수
main()
이 모든 기능을 조정하고 사용자가 프로그램을 다시 시작하거나 종료할 수 있게 합니다.
이 코드는 사용자 입력을 기반으로 데이터를 필터링하고, 자전거 공유 서비스에 대한 다양한 통계를 계산하여 제공합니다
"""