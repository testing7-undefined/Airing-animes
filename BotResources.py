import requests

#======================================================================================#

class newEpisodesAnimes:

  def __init__(self) :
    pass

#today airing animes
  def todayAiringAnimes(self):
    #get today airing animes from subsplease.org api
    url = "https://subsplease.org/api/?f=schedule&h=true&tz=Asia/Kolkata"
    response = requests.get(url)

    if response.status_code == 200:
      response = response.json()
      return response
    
    return None
  

#poster of anime
  def poster(self,id):
    url = f"https://img.anili.st/media/{id}"
    response = requests.get(url)

    if response.status_code == 200:
      return response.content
    return None

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#kitsu data
  def kitsuData(self, name):
    # URL of the Kitsu API endpoint for anime
    url = 'https://kitsu.io/api/edge/anime'

    # Headers as per the JSON:API specification
    headers = {
      'Accept': 'application/vnd.api+json',
      'Content-Type': 'application/vnd.api+json'
    }

    # Query parameters for filtering by category
    params = {
      'filter[text]': f'{name}' 
    }

    # Making the GET request
    response = requests.get(url, headers=headers, params=params)

    # Checking the response status code
    if response.status_code == 200:
        # Print the response content
        response = response.json()
        return response
    
    return None


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


#anilist id and anime name
  def anilistData(self, name):
    # Here we define our query as a multi-line string
    query = '''
    query($search: String){
      Page(page: 1, perPage: 20){
        media(search: $search, type: ANIME){
          id
          title {
            romaji
            english
            native
            userPreferred
          }
          status
          season
          startDate {
            year
            month
            day
          }
          endDate {
            year
            month
            day
          }
          nextAiringEpisode{
            episode
          }
        }
      }
    }
    '''
    # Define our query variables and values that will be used in the query request
    variables = {
        'search' : f'{name}'
    }

    url = 'https://graphql.anilist.co'

    # Make the HTTP Api request
    response = requests.post(url, json={'query': query, 'variables': variables})
    if response.status_code != 200:
      return None
    
    animes = response.json()["data"]["Page"]["media"]
    # print(animes)
    for anime in animes:
      # print(anime["startDate"], anime["endDate"])
      if anime["status"] != "RELEASING":
        continue  

      return anime
      
    return None



    
    
    
########################################################################################


class getData(newEpisodesAnimes):

  message = """
*{}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
‣ Time:* `{}` GMT
*‣ Language:* `Japanese [ESub]`
*‣ Season:* `{}`
*‣ Episode:* `{}`
*‣ Synopsis:* `{}`
*━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━*
"""
  
  def __init__(self):
    pass

#updating new message 
  def updateMessage(self, message:str):
    newMessage:str = ""

    for character in message:
      if character.isalnum() or character == ' ' or character == '/' :
        newMessage += character
        continue
      newMessage += rf'\{character}'
    
    return newMessage
  
# message data
  def messageData(self):

    todayAnimes = self.todayAiringAnimes()

    if not todayAnimes:
      return None
    
    print("Today anime list Collected Successfully\n")

    animeData = []

    for anime in todayAnimes["schedule"]:
      title = anime["title"]
      
      tempData = {
        'substitle' : title,
        'time': anime["time"]
      }
      
      
    #awaiting for receving of anilist data
      originalData = self.anilistData(title)
      if not originalData :
        continue
      
      print(f"{title} : data from Ai Collected successfully")

      originalName:str = originalData["title"]["romaji"]

      #print(originalData)

      tempData.update({
        'titles' : self.updateMessage(originalData["title"]["english"]),
        'posterId' : f'{originalData["id"]}',
        'season' : f'{originalData["season"]}',
        'episode' : originalData["nextAiringEpisode"]["episode"] 
      })

    #awaiting for receving of kitsudata
      kitsuData = self.kitsuData(originalName)
      if not kitsuData:
        continue

      print(f"{title} : data from Kl Collected successfully\n")
      kitsuData = kitsuData['data'][0]
      tempData["synopsis"] = kitsuData["attributes"]["synopsis"]


      animeData.append(tempData)

    #print(animeData)
    print("Collected anime data sent to bot function Successfully")
    if not animeData :
      return None
    return animeData


##############################################################################





def main():
  today = getData()
  # result = today.anilistData("Boukyaku Battery")
  # print(result)
  today.messageData()
  # print(today.updateMessage("? ! hi "))
 

if __name__ == '__main__':
  main()