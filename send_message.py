import time
import pywhatkit
numbers = [679185270, 679567170, 653957807, 672837586, 650367408, 672304579, 650369408, 672384578, 674787814, 678772649, 623137649, 679726064, 672384529, 651516229, 672754178, 691327257,  677860275, 678113959, 671234567, 699281457, 672381579, 652387594, 682758875, 690771391, 650700767, 6219584, 683696435, 654456483, 679341471,  623164973, 681270314, 651975585, 650970348, 673866040, 651140080, 678656088, 654599365, 678619941, 653761228, 674391456, 651062315, 683229963, 670010358, 682640802, 678709609, 670865568, 681143067, 651443610, 654134008, 680386520, 650844550, 674181399, 671312568, 653750492,  683532083, 676668463, 653004900, 673133347, 672792563, 673277803, 678591851, 682090879, 681502670, 652267455, 676729756, 678093750, 681537466, 672431353, 652774198, 679582898, 677546481]

def senn_message():
    message = '''
        Hi 
I see you've joined *Z-learn* (great choice! ), but you haven’t yet registered for any entrance exam. Just curious
👉 Is there something you're unsure about?  
👉 Need help choosing the right exam or understanding how it works?

We’ve got powerful tools and resources waiting for you such as past questions, exam tips, and more  all designed for success in competitive exams like *Medicine, Nursing, NAHPI, FET*, etc. 



Let’s make your goal a reality!

Z-learn Team
'''

    for number in numbers:
        print(f'sendeing message to {number}')
        pywhatkit.sendwhatmsg_instantly(f'+237{number}',message )
        time.sleep(40)

if __name__ == "__main__":
    senn_message()