import schedule
import time


def job(a, b, c):
    print("I'm working...", a, b, c)


# schedule.every(5).minutes.do(job, 1, 2, 3)
# schedule.every(10).minutes.do(job)
# schedule.every().hour.do(job)
schedule.every().day.at("19:00").do(job,1,3,7)
schedule.every().day.at("18:59").do(job,1,3,6)
schedule.every().day.at("18:58").do(job,1,3,6)


while 1:
    schedule.run_pending()
    time.sleep(1)
