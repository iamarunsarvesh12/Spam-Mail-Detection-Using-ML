"""
augment_dataset.py
--------------------
Adds extra, realistic EMAIL-style examples (both spam and not-spam/ham) to
the existing dataset. The original dataset (spam_dataset.tsv) was SMS-based;
this adds longer, email-formatted messages so the model generalizes better
to actual emails, per the project's use case.

Run this once from inside the data/ folder:
    python augment_dataset.py
It appends new rows to spam_dataset.tsv (does not remove any existing data).
"""

SPAM_EMAILS = [
    "Congratulations! You have been selected to receive a $1000 Walmart gift card. Click here to claim your prize now before it expires.",
    "URGENT: Your account has been suspended due to unusual activity. Verify your identity immediately by clicking this link or your account will be permanently closed.",
    "You have won the UK National Lottery! Reply with your full name, address, and bank details to claim your prize of £2,500,000.",
    "Dear Winner, your email address has won you 850,000 Euros in the Microsoft Online Lottery Promo. Contact our claims agent immediately to process your winnings.",
    "Get rich quick! Work from home and earn $5000 per week with no experience required. Limited spots available, sign up now!",
    "Your PayPal account has been limited. Please confirm your billing information within 24 hours to avoid permanent suspension of your account.",
    "FINAL NOTICE: Your car's extended warranty is about to expire. Call now to renew and save 50% on your coverage plan.",
    "Hot singles in your area are waiting to chat with you right now! Click here to view profiles near you, totally free.",
    "Buy cheap Viagra online without prescription. Fast discreet shipping worldwide. Order now and save up to 80% off retail price.",
    "You've been pre-approved for a $50,000 loan with 0% interest for the first year. No credit check required. Apply within 48 hours.",
    "Nigerian prince here. I need your help to transfer 18.5 million dollars out of my country. You will receive 30% of the total amount for your assistance.",
    "Limited time offer: Lose 20 pounds in 2 weeks with this one weird trick doctors don't want you to know about. Order your supply today.",
    "Your Netflix subscription payment failed. Update your payment details immediately or your account will be suspended within 24 hours.",
    "CONGRATULATIONS! Your phone number has been randomly selected to win an iPhone 15 Pro. Claim your free gift now, only pay shipping.",
    "Make $300 a day taking simple surveys online from home. No experience needed, sign up free and start earning today.",
    "Your Amazon order could not be delivered. Click here to update your shipping address and reschedule delivery immediately.",
    "Investment opportunity of a lifetime! Turn $500 into $50,000 in 30 days with our proven crypto trading algorithm. Act fast, limited spots.",
    "IRS Notice: You owe back taxes and a warrant has been issued for your arrest. Call this number immediately to resolve this matter before legal action.",
    "Free trial! Get whiter teeth in just 7 days with our revolutionary teeth whitening kit. Pay only shipping and handling, cancel anytime.",
    "Your computer has been infected with 5 viruses. Download our antivirus software immediately to protect your personal information from hackers.",
    "Exclusive offer just for you: refinance your mortgage today and save thousands. Rates are at an all time low, act before they rise again.",
    "You have 1 new voicemail from an unknown caller regarding your vehicle's extended warranty. Press 1 now to speak with a representative.",
    "Earn a college degree from home in 5 days, no coursework required. Diplomas accepted by employers worldwide, order yours today.",
    "Act now! This is not a scam. Send $99 processing fee to claim your inheritance of 3.2 million dollars from a distant relative.",
    "Your Apple ID has been locked for security reasons. Click the link below within 24 hours to restore full access to your account.",
    "Free cruise vacation for two! You have been selected among thousands. Call now to claim your all expenses paid trip to the Bahamas.",
    "Hurry! Only 3 items left in stock. Get 90% off designer watches today only, free shipping worldwide, order before midnight.",
    "Dear valued customer, your bank account will be closed unless you update your KYC details by clicking the secure link provided below.",
    "You are pre-selected for a free credit card with a $10,000 limit and no annual fee. Approval guaranteed regardless of your credit history.",
    "Work from anywhere and be your own boss! Join our team today and start making six figures within your first month, no experience necessary.",
    "Your package is on hold due to unpaid customs fee of $2.99. Click here to pay now and release your shipment immediately.",
    "WINNER WINNER! Your name was drawn in our monthly prize giveaway. Claim your brand new laptop by confirming your shipping details now.",
    "This is your final chance to lower your student loan payments by up to 60%. Call our specialists today before the offer expires.",
    "Get a free vacation home trial! Attend our 90 minute presentation and receive a complimentary weekend getaway plus $100 cash.",
    "Alert: unusual sign-in activity detected on your account from a new device. Verify it was you by entering your password here immediately.",
]

HAM_EMAILS = [
    "Hi team, just a reminder that our weekly sync is moved to 10am tomorrow instead of 9am. Please update your calendars accordingly.",
    "Hey, are we still on for lunch tomorrow? Let me know what time works best for you and I'll book the table.",
    "Attached is the revised budget spreadsheet for Q3. Let me know if the numbers look correct before I send it to finance.",
    "Thanks for sending over the report. I've reviewed it and left a few comments in the margins, mostly minor suggestions.",
    "Reminder: your dentist appointment is scheduled for Thursday at 2:30pm. Please arrive 10 minutes early to fill out paperwork.",
    "Hi Sarah, following up on our call yesterday, I've attached the contract draft. Let me know if you have any questions.",
    "The project deadline has been extended to next Friday. Please update your task list and let the team know if you need help.",
    "Good morning! Just confirming our meeting for 3pm today in conference room B. Looking forward to discussing the proposal.",
    "Can you send me the notes from yesterday's client meeting? I want to make sure I didn't miss anything important.",
    "Happy birthday! Hope you have a wonderful day. Let's grab coffee sometime next week to celebrate properly.",
    "Your flight booking is confirmed for December 15th. Departure at 8:45am from Terminal 2. Please check in online 24 hours before.",
    "Hi Professor, I wanted to ask if I could get an extension on the assignment due to a family emergency this week.",
    "The quarterly newsletter is now live on our website. It covers updates on the new product launch and upcoming events.",
    "Thanks for the feedback on my presentation, I'll incorporate your suggestions before the final version is due next Monday.",
    "Reminder: parent-teacher conferences are scheduled for next Tuesday from 4pm to 7pm. Please sign up for a time slot online.",
    "Hey, just checking in to see how the move went. Let me know if you need any help unpacking this weekend.",
    "Please find attached the invoice for last month's services. Payment is due within 30 days as per our agreement.",
    "Great catching up with you at the conference last week. Let's schedule a follow-up call to discuss potential collaboration.",
    "The gym will be closed this Sunday for maintenance. Regular hours resume Monday morning at 6am as usual.",
    "I've updated the shared document with the latest sales figures. Take a look when you get a chance and let me know your thoughts.",
    "Your order has shipped and is expected to arrive within 3-5 business days. You can track your package using the link in your account.",
    "Hi, just wanted to confirm you received my last email about the schedule change. Let me know if that works for you.",
    "The book club meeting is this Thursday at 7pm at my place. We're discussing chapters 5 through 8, snacks provided as usual.",
    "Congratulations on completing the certification! Your hard work really paid off, well deserved recognition from the whole team.",
    "Please review the attached meeting minutes and let me know if I missed anything or if any action items need clarification.",
    "Reminder that the office will be closed on Monday for the public holiday. Normal operations resume Tuesday morning.",
    "Thanks for helping me move last weekend, I really appreciate it. Let me buy you dinner sometime to say thanks properly.",
    "The library books you requested are ready for pickup. Please collect them within 5 days or the reservation will be cancelled.",
    "I wanted to follow up on the interview from last week. We'd love to schedule a second round with the team if you're available.",
    "Here's the itinerary for our trip next month, including hotel confirmations and the rental car pickup details.",
    "Hi, could you review my pull request when you get a chance? I made the changes we discussed in yesterday's standup.",
    "The school fundraiser raised over $3000 this year, thank you to everyone who volunteered and donated to make it a success.",
    "Just a heads up, the wifi in the office will be down for scheduled maintenance tonight from 11pm to 1am.",
    "Looking forward to seeing you at the wedding next month! Let me know if you need help with directions to the venue.",
]

if __name__ == "__main__":
    lines = []
    for msg in SPAM_EMAILS:
        lines.append(f"spam\t{msg}")
    for msg in HAM_EMAILS:
        lines.append(f"ham\t{msg}")

    with open("spam_dataset.tsv", "a", encoding="utf-8") as f:
        f.write("\n" + "\n".join(lines) + "\n")

    print(f"Added {len(SPAM_EMAILS)} spam and {len(HAM_EMAILS)} ham email examples.")
    print(f"Total new rows added: {len(lines)}")
