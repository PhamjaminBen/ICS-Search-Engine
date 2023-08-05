import index
import search
import time
import PySimpleGUI as sg
import sys

#THIS IS THE MAIN MODULE TO RUN TO EXECUTE THE SEARCH ENGINE
#ALL OTHER MODULES CONTAIN if __name__ == '__main__' FOR TESTING

spacing = '================================= BEN PHAM // CHARLIE ZHAO //SEARCH ENGINE ================================='


def display():
    layout = [ [sg.Text('Enter Query:'), sg.Input(size = (45,1), key='IN')], 
            [sg.Text('', key='TOP')], [sg.Text('', key='NUM')], [sg.Text('', key='OUT')],
            [sg.Button('Enter'), sg.Button('Exit'), sg.Button('Next'), sg.Button('Prev')] ]

    window = sg.Window("BP CZ Search Engine", layout)

    first = False
    while True:
        event, values = window.read()
        if event == 'Exit' or event == sg.WIN_CLOSED:
            break
        
        if event == 'Enter':
          first = True
          window['OUT'].update('')
          window['TOP'].update('')
          window['NUM'].update('')

          #query section
          query = values['IN']

          #begin timer
          t1 = time.perf_counter()

          #get all the tf-idf scores of the documents
          intersect = search.Search(query)

          #end timer and calculate search time elapsed
          t2 = time.perf_counter()
          elapsed = t2-t1

          #sort docs by tf-idf score after timing the search

          top = f'{len(intersect)} results found in {round(elapsed,3)} seconds ({round(elapsed*1000,2)} ms)'
          window['TOP'].update(top)

          #sorting by total score
          intersect = search.matchID(intersect)
          intersect.sort(key = lambda x: -x[1]-0.5*x[2])

          ret = ''
          c = 0
          show = f'Displaying results {c+ 1} to {c+10}'
          for i, (url, score, pagerank) in enumerate(intersect[c:c+10],c+1):
            ret += f'{i}. {url} (tf-idf: {score}, pagerank: {round(0.5*pagerank,3)}, total: {round(score+0.5*pagerank,3)}) \n'
          print(ret)
          window['OUT'].update(ret)
          window['NUM'].update(show)

        if event == 'Next':
          #go to next 10
          if not first: continue

          ret = ''
          if(c+10 < len(intersect)):
            c += 10
          show = f'Displaying results {c+1} to {c+10}'
          for i, (url, score, pagerank) in enumerate(intersect[c:c+10],c+1):
            ret += f'{i}. {url} (tf-idf: {score}, pagerank: {round(0.5*pagerank,3)}, total: {round(score+0.5*pagerank,3)}) \n'
          print(ret)
          window['OUT'].update(ret)
          window['NUM'].update(show)
        
        if event == 'Prev':
          #go to previous 10
          if not first: continue

          ret = ''
          if(c>0):
            c -= 10
          show = f'Displaying results {c+1} to {c+10}'
          for i, (url, score, pagerank) in enumerate(intersect[c:c+10],c+1):
            ret += f'{i}. {url} (tf-idf: {score}, pagerank: {round(0.5*pagerank,3)}, total: {round(score+0.5*pagerank,3)}) \n'
          
          print(ret)
          window['OUT'].update(ret)
          window['NUM'].update(show)
          
    window.close()


if __name__ == '__main__':
  #reindex if needed
  #prompt in console
  print(spacing)
  reset = input('Reindex webpages? (Y/N): ')
  if reset == 'Y':
    debug = input('Print debug statements? (Y/N): ')
    b = False
    if debug == 'Y':
      b = True
    index.index(b)

  print('Initiating search engine...')

  #GUI using PySimpleGUI with function calls to receive query 
  #and search with indexed files
  display()

  print('Shutting down...')
  print(spacing)
  sys.exit()




    
