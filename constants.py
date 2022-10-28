columns = ['date', 'time', 'location', 'title', 'artists', 'works', 'imageLink']

classNames = {
  # The same class contains date, time, location and works of each event.
  "eventDetails": "cell xlarge-6 body-small",
  # The same tag includes both title as well as the artists names.
  "eventDescription": "event-title h3",
  "imageLink":"clr-sec"
}

url = 'https://www.lucernefestival.ch/en/tickets/program'
domain = 'www.lucernefestival.ch'
