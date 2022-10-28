from bs4 import BeautifulSoup
import pandas as pd 

import requests
import constants as constants
import connection as loadDatabase


scrappedData = pd.DataFrame()
html_text = requests.get(constants.url).text
soup = BeautifulSoup(html_text, 'lxml')

# Scrap all the required data.
eventsDetails = soup.find_all('div', class_ = constants.classNames['eventDetails'])
eventDescription = soup.find_all('p', class_ = constants.classNames['eventDescription'])
eventsImageLink = soup.find_all('picture', class_ = constants.classNames['imageLink'])


###########
def main():

  # Store all the data into a data frame.
  add_event_details(eventsDetails)
  add_event_description(eventDescription)
  add_event_image_link(eventsImageLink)

  records = scrappedData.to_records(index=False)
  result = list(records)

  # Connect to the database, create the table and store the data.
  loadDatabase.connect_and_load_data(result)



##################################
def convert_works_to_string(works):
  combinedWorks = ''
  for work in works:
    combinedWorks += work

  return combinedWorks.strip()

####################################################################
def add_to_data_frame(dataFrame, rowIndex, columnName, data):
  dataFrame.at[rowIndex, columnName] = data
  return dataFrame

#####################################
def add_event_details(eventsDetails):
  eventCounter = 0
  for  event in eventsDetails:
    if event.find('br') is not None:
      df = {}
      cleanedList = (event.strong.text + "|" + " ".join(event.find('br').next_sibling.split())).split("|")

      # Some events do not have any works mentioned.
      if cleanedList[0] == 'Date and Venue':
        add_to_data_frame(scrappedData, eventCounter, 'Date', cleanedList[1].strip())
        add_to_data_frame(scrappedData, eventCounter, 'Time', cleanedList[2].strip())
        add_to_data_frame(scrappedData, eventCounter, 'Location', cleanedList[3].strip())
      elif cleanedList[0] == 'Program':
        # Some events have more than one work.
        df['Works'] = cleanedList[1:]
        eventCounter -= 1
        combinedWorks = convert_works_to_string(df['Works'])
        add_to_data_frame(scrappedData, eventCounter, 'Works', combinedWorks)

      eventCounter += 1

###########################################
def add_event_description(eventDescription):
  for index, eventDescription in enumerate(eventDescription):
    cleanedList = (eventDescription.find('a').text).split("|")
    add_to_data_frame(scrappedData, index, 'Title', cleanedList[0])
    if(len(cleanedList) > 1):
      add_to_data_frame(scrappedData, index, 'Artists', ' '.join(cleanedList[1:]))


################################
def decode_image_url(image_url):
  return constants.domain + image_url



#########################################
def add_event_image_link(eventsImageLink):
  for index, eventImageLink in enumerate(eventsImageLink):
    decoded_image_url = decode_image_url(eventImageLink.find('source')['srcset'])
    add_to_data_frame(scrappedData, index, 'ImageLink', decoded_image_url)


main()


