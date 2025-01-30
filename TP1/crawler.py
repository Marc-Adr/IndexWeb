import json
import time
from urllib.parse import urljoin, urlparse
from urllib.request import urlopen, Request
from urllib.robotparser import RobotFileParser
from bs4 import BeautifulSoup

class Crawler:
    def __init__(self, url_start, pages_max=50, name="MarcRobot"):
        """
        Initialise le crawler avec :
        - l'URL de départ
        - le nombre maximum de pages à visiter
        - l'agent utilisateur pour les requêtes HTTP
        """
        self.url_start = url_start
        self.pages_max = pages_max
        self.data = []  # Stockage des résultats
        self.crawler_name = name # Le nom du crawler
        

    def get_html(self, url):
        """
        Récupère le contenu HTML d'une page donnée si c'est autorisée.
        """

        robots_parser = RobotFileParser() # Initialisation du parser robots.txt pour respecter les règles du site
        robots_parser.set_url(urljoin(self.url_start, "/robots.txt"))
        robots_parser.read()
        if not robots_parser.can_fetch(self.crawler_name, url): # Vérifie si le crawler a la permission d'accéder à une URL
            print(f"Accès interdit par robots.txt: {url}")
            return None
        
        req = Request(url)
        response = urlopen(req)
        return response.read() # Retourne l'HTML du lien
    
    def parse_html(self, url, html):
        """
        Analyse le contenu HTML et extrait :
        - Le titre de la page
        - Le premier paragraphe trouvé
        - La liste des liens internes du site
        """
        soup = BeautifulSoup(html, 'html.parser')
        title = ""
        if soup.title: # S'il y a un titre, sinon le titre est ""
            title = soup.title.string
        paragraphs = soup.find('p')
        first_paragraph = ""
        if paragraphs: # Même chose pour les paragraphes
            first_paragraph = paragraphs.text
        links = []
        for a in soup.find_all('a', href=True): # Recherche des balises contenant href pour avoir des url
            links.append(urljoin(url, a['href'])) # Ajout du lien
        
        return {
            'title': title,
            'url': url,
            'first_paragraph': first_paragraph,
            'links': links
        }
    
    def save_data(self):
        """
        Enregistre les résultats du crawl dans un fichier JSON.
        """
        with open("resultat.json" ,"w", encoding='utf-8') as file:
            json.dump(self.data, file)
    
    def crawl(self):
        """
        Parcourt les pages du site en respectant :
        - La limite de pages à visiter
        - Une priorité pour les liens contenant 'product'
        """
        visited_urls = []  # Ensemble des URLs déjà visitées 
        to_visit =[self.url_start] # Liste des URLs à visiter

        while to_visit and len(visited_urls) < self.pages_max: # S'il nous reste des url à visiter et qu'on a pas visité 50 urls
            url= to_visit.pop(0) # Récupérer la prochaine URL à visiter
            if url in visited_urls:
                continue  # Ignorer si l'URL a déjà été visitée
            
            print(f"Visite: {url}") # Suivre l'avancement du crawler
            html = self.get_html(url)  # Télécharger la page
            if html:
                page_data = self.parse_html(url, html)  # Extraire les informations utiles
                self.data.append(page_data)
                visited_urls.append(url)
                
                # Prioriser les liens vers des pages produits
                for link in page_data["links"]:
                    if "/product/" in link :
                        to_visit.insert(0,link) # Ajoute les "products" au début de la liste pour que pop(0) retourne les products en prio
                    else:
                        to_visit.append(link)

                
                time.sleep(1)  # Pause pour éviter de surcharger le serveur (politesse)
        
        self.save_data()
