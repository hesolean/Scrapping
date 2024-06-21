# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import re
from itemadapter import ItemAdapter

from .database import SessionLocal
from .models import Gender, Language, Media, Person, Serie

class MoviesscraperPipeline:
    def process_item(self, item, spider):
        # item = self.cleaning_title(item)
        item = self.cleaning_original_title(item)
        item = self.cleaning_score(item)
        item = self.cleaning_gender(item)
        item = self.cleaning_duration(item)
        item = self.cleaning_description(item)
        item = self.cleaning_director(item)
        item = self.cleaning_year(item)
        return item

    def cleaning_title(self, item):
        adapter = ItemAdapter(item)

        # je garde ce qui est entre guillemets
        motif = r'\(".*?"\)'
        title = adapter.get('title')

        # je n'applique le test que s'il y a des guillemets
        if title and '"' in title:
            cleaned_title = re.sub(motif, '', title).strip()
            adapter['title'] = cleaned_title
        return item
    
    def cleaning_original_title(self, item):
        adapter = ItemAdapter(item)

        # je garde ce qui est après les : sans l'espace
        motif = r':\s*(.*)'
        original_title = adapter.get('original_title')

        if original_title is None:
            return item
        
        cleaned_title = re.search(motif,original_title).group(1)
        adapter['original_title'] = cleaned_title
        return item
    
    def cleaning_score(self, item):
        adapter = ItemAdapter(item)

        score = adapter.get('score')

        # je n'applique la modification que si le score existe et qu'il est en string
        if score and isinstance(score, str):
            # je transforme en float
            cleaned_score = score.replace(',', '.')
            adapter['score'] = cleaned_score
        return item
    
    def cleaning_gender(self, item):
        adapter = ItemAdapter(item)
        genders = adapter.get('gender')
        
        # je définis une liste vide pour le nettoyage
        cleaned_gender = []

        # je retire le dernier élément de la liste s'il est écrit Retour en heut de la page
        for gender in genders:
            if gender == 'Retour en haut de la page':
                break
            cleaned_gender.append(gender)
        adapter['gender'] = cleaned_gender
        return item
    
    def cleaning_duration(self, item):
        adapter = ItemAdapter(item)
        # je récupère indépendemment les chiffres avant h et ceux avant min
        motif_heures = r'(\d+)h'
        motif_minutes = r'(\d+)m'
        duration = adapter.get('duration')
    
        # j'initialise les variables
        minutes = 0
        minutes_heure = 0

        # je récupère les heures et les convertis en minutes
        if duration and 'h' in duration:
            minutes_heure = int(re.search(motif_heures, duration).group(1)) * 60

        # je récupère les minutes
        if duration and 'm' in duration:
            minutes = int(re.search(motif_minutes, duration).group(1))

        # je les additionne
        cleaned_duration = minutes_heure + minutes
        adapter['duration'] = cleaned_duration
        return item
    
    def cleaning_description(self, item):
        adapter = ItemAdapter(item)

        # je garde ce qui est entre guillemets
        motif = r'\(".*?"\)'
        description = adapter.get('description')
        
        # je n'applique le test que s'il y a des guillemets
        if description and '"' in description:
            cleaned_description = re.sub(motif, '', description).strip()
            adapter['description'] = cleaned_description
        return item

    def cleaning_director(self, item):
        adapter = ItemAdapter(item)
        director = adapter.get('director')

        adapter['director'] = director
        return item
    
    def cleaning_year(self, item):
        adapter = ItemAdapter(item)
        year = adapter.get('year')

        # je nettoie la chaine de caractères et garde les 4 derniers elements de la liste
        value = ''.join(year).strip()
        cleaned_year = value[:4]

        adapter['year'] = cleaned_year
        return item
    
class Allo(MoviesscraperPipeline):
    def cleaning_duration(self, item):
        adapter = ItemAdapter(item)
        
        # je récupère indépendemment les chiffres avant h et ceux avant min
        motif_heures = r'(\d+)h'
        motif_minutes = r'(\d+)m'
        duration = adapter.get('duration')

        value = ''.join(duration).strip()
        # j'initialise les variables
        minutes = 0
        minutes_heure = 0

        # je récupère les heures et les convertis en minutes
        if value and 'h' in value:
            minutes_heure = int(re.search(motif_heures, value).group(1)) * 60

        # je récupère les minutes
        if value and 'm' in value:
            minutes = int(re.search(motif_minutes, value).group(1))

        cleaned_duration = minutes + minutes_heure
        adapter['duration'] = cleaned_duration
        return item
    
    def cleaning_director(self, item):
        adapter = ItemAdapter(item)
        director = adapter.get('director')

        # je garde le 2ème element de la liste
        cleaned_director = director[1]
        adapter['director'] = cleaned_director
        return item
    
    def cleaning_year(self, item):
        adapter = ItemAdapter(item)
        year = adapter.get('year')

        # je nettoie la chaine de caractères et garde les 4 derniers elements de la liste
        value = ''.join(year).strip()
        cleaned_year = value[-4:]
        adapter['year'] = cleaned_year
        return item

    def cleaning_original_title(self, item):
        adapter = ItemAdapter(item)
        original_title = adapter.get('original_title')

        if original_title is None:
            return item
        
        adapter['original_title'] = original_title
        return item
''' 
commande de terminal pour lancer une image mysql avec docker
docker run --name mysql-container -e MYSQL_ROOT_PASSWORD=rootpassword -e MYSQL_DATABASE=mydatabase -e MYSQL_USER=myuser -e MYSQL_PASSWORD=mypassword -p 3306:3306 -d mysql:latest

base de données de test
docker run --name mysql-test -e MYSQL_ROOT_PASSWORD=rootpassword -e MYSQL_DATABASE=testdb -e MYSQL_USER=testuser -e MYSQL_PASSWORD=testpassword -p 3306:3306 -d mysql:latest

'''
class DatabasePipeline:
    def __init__(self):
        self.Session = SessionLocal

    def open_spider(self, spider):
       self.session = self.Session()
    
    def process_item(self, item, spider):
        #  détermination de type en fonction du spider
        if spider.name == 'moviesspider':
            media_type = "movie"
        elif spider.name == 'seriesspider':
            media_type = "serie"
        else:
            media_type = None
        
        # récupération des médias
        media = Media(
            title=item['title'],
            original_title = item['original_title'],
            score = item['score'],
            year = item['year'],
            duration = item['duration'],
            description = item['description'],
            public = item['public'],
            country = item['country'],
            type = media_type
        )

        # ajout de media pour obtenir son ID
        self.session.add(media)
        self.session.commit()

        # récupération des langues
        languages = item['language']
        for language in languages:
            existe_language = self.session.query(Language).filter_by(language=language).first()
            if not existe_language:
                existe_language=Language(language=language)
                self.session.add(existe_language)
            media.languages.append(existe_language)
        
        # récupération des genres
        genders = item['gender']
        for gender in genders:
            existe_gender = self.session.query(Gender).filter_by(gender=gender).first()
            if not existe_gender:
                existe_gender=Gender(gender=gender)
                self.session.add(existe_gender)
            media.genders.append(existe_gender)
        
        # ajout des acteurs
        actors = item['actors']
        for actor in actors:
            self.add_person(actor, role='actor', media=media)

        # ajout des réalisateurs
        directors = item['director']
        for director in directors:
            self.add_person(director, role='director', media=media)
        
        # ajout des séries
        if spider.name == 'seriesspider':
            serie = Serie(
                media_id = media.id,
                seasons = item['nb_seasons'],
                episodes = item['nb_episodes']
            )
            self.session.add(serie)

        # mise à jour des ajouts
        self.session.commit()
        return item
    
    # fonction pour l'ajout d'acteurs et directeurs
    def add_person(self, name, role, media):
        name_parts = name.split()

        # je gère les noms composés
        if len(name_parts) == 1:
            first_name = name
        elif len(name_parts) == 2:
            first_name, last_name = name.split()
        else:
            first_name = name[0]
            last_name = ' '.join(name_parts[1:])

        exist_person = self.session.query(Person).filter_by(first_name=first_name, last_name=last_name).first()
        if not exist_person:
            exist_person = Person(first_name=first_name, last_name=last_name, role=role)
            self.session.add(exist_person)
        media.persons.append(exist_person)
        
        

    def close_spider(self, spider):
        self.session.close()