from database import ReminderDetails, session as sess

reminders = sess.query(ReminderDetails).all()
for reminder in reminders:
    print(type(reminder.rent_expiry_date))
    