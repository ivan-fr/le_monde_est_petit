import program.world as script
import pytest
    
def hello(name):
    return 'Hello ' + name

def test_hello():
    assert hello('Celine') == 'Hello Celine'


#############################################
################## AGENT ####################
#############################################

class TestAgent:
    def setup_method(self):
        self.AGENT = script.Agent(3)

    # - Agent : 
    #   - récupérer un attribut position
    def test_set_position(self):
        self.AGENT.position = 5
        assert self.AGENT.position == 5

    #   - modifier un attribut position
    def test_get_position(self):
        assert self.AGENT.position == 3

    #   - assigner un dictionnaire en tant qu'attributs
    def test_set_agent_attributes(self):
        dictionary = {"agreeableness": -1}
        agent = script.Agent(3, **dictionary)
        assert agent.agreeableness == -1


#############################################
################# POSITION ##################
#############################################

class TestPosition:
    def setup_method(self):
        self.POSITION = script.Position(100, 33)

    # - Position :
    #   - modifier un attribut longitude_degrees
    def test_longitude_degrees(self):
        assert self.POSITION.longitude_degrees == 100

    #   - modifier un attribut latitude_degrees
    def test_latitude_degrees(self):
        assert self.POSITION.latitude_degrees == 33

    #   - modifier un attribut longitude_degrees avec une valeur supérieure à 180 renvoie une erreur.
    def test_longitude_degrees_range(self):
        with pytest.raises(AssertionError):
            script.Position(200, 33)

    #   - modifier un attribut latitude_degrees avec une valeur supérieure à 90 renvoie une erreur.
    def test_latitude_degrees_range(self):
        with pytest.raises(AssertionError):
            script.Position(100, 100)

    #   - récupérer une longitude
    def test_longitude(self):
        assert self.POSITION.longitude == 1.7453292519943295

    #   - récupérer une latitude
    def test_latitude(self):
        assert self.POSITION.latitude == 0.5759586531581288


#############################################
################### ZONE ####################
#############################################

class TestZone:

    def setup_method(self):
        self.POSITION1 = script.Position(100, 33)
        self.POSITION2 = script.Position(101, 34)  
        self.ZONE = script.Zone(self.POSITION1, self.POSITION2)
        script.Zone._initialize_zones()
        agent = script.Agent(self.POSITION1, agreeableness=1)
        self.ZONE.inhabitants = [agent]

    def teardown_method(self):
        self.ZONES = []

    #   - récupérer toutes les instances Zone (Zone.ZONES)
    # On devrait avoir exactement 64800 zones
    def test_get_zones(self):
        assert len(script.Zone.ZONES) == 64800

    # - Zone :
    def test_zone_that_contains(self):
        position = self.POSITION1
        found_zone = script.Zone.find_zone_that_contains(position)
        assert position.longitude >= min(found_zone.corner1.longitude, found_zone.corner2.longitude)
        assert position.longitude < max(found_zone.corner1.longitude, found_zone.corner2.longitude)
        assert position.latitude >= min(found_zone.corner1.latitude, found_zone.corner2.latitude)
        assert position.latitude < max(found_zone.corner1.latitude, found_zone.corner2.latitude)


    #   - trouver une zone qui contient une position
    def test_find_zone_that_contains(self):
        found_zone = script.Zone.find_zone_that_contains(self.POSITION1)
        assert found_zone.contains(self.POSITION1)

    #   - ajouter un habitant dans une zone
    def test_add_inhabitant_in_zone(self):
        agent = script.Agent(self.POSITION1, agreeableness=1)
        self.ZONE.add_inhabitant(agent)
        assert len(self.ZONE.inhabitants) == 2


    #   - récupérer la densité de population d'une zone
    def test_get_population_density(self):
        assert self.ZONE.population_density() == 8.087793508722422e-05

#   - récupérer l'agréabilité moyenne d'une zone
    def test_get_average_agreeableness(self):
        assert self.ZONE.average_agreeableness() == 1


class TestAgreeablenessGraph:
# - AgreeablenessGraph :

    def setup_method(self):
        script.Zone._initialize_zones()
        self.ZONE = script.Zone.ZONES[0]
        self.GRAPH = script.AgreeablenessGraph()
        self.ZONES = script.Zone.ZONES
        for _ in range(0, 10):
            self.ZONE.add_inhabitant(script.Agent(script.Position(-180, -89), agreeableness=1))

#   - récupérer un titre
    def test_title(self):
        assert self.GRAPH.title == 'Nice people live in the countryside'

#   - récupérer x_label
    def test_x_label(self):
        assert self.GRAPH.x_label == 'population density'

#   - récupérer y_label
    def test_y_label(self):
        assert self.GRAPH.y_label == 'agreeableness'

#   - récupérer xy_values sous forme de tuples
    def test_xy_values(self):
        assert len(self.GRAPH.xy_values(self.ZONES)) == 2

#   - la première valeur de xy_values est la densité de population moyenne pour la première zone
    def test_average_population_density(self):
        assert self.GRAPH.xy_values(self.ZONES)[0][0] == self.ZONE.population_density()

#   - la seconde valeur de xy_values est l'agréabilité moyenne
    def test_average_agreeableness(self):
        assert self.GRAPH.xy_values(self.ZONES)[1][0] == self.ZONE.average_agreeableness()

class TestIncomeGraph:

    def setup_method(self):
        script.Zone._initialize_zones()
        self.ZONE = script.Zone.ZONES[0]
        self.GRAPH = script.IncomeGraph()
        self.ZONES = script.Zone.ZONES
        for _ in range(0, 10):
            self.ZONE.add_inhabitant(script.Agent(script.Position(-180, -89), income=40, age=20))

    def test_title(self):
        assert self.GRAPH.title == 'Older people have more money'

    def test_x_label(self):
        assert self.GRAPH.x_label == 'age'

    def test_y_label(self):
        assert self.GRAPH.y_label == 'income'

    def test_xy_values(self):
        assert len(self.GRAPH.xy_values(self.ZONES)) == 2

    def test_age(self):
        assert self.GRAPH.xy_values(self.ZONES)[0][20] == 20

    def test_average_income_by_age(self):
        assert self.GRAPH.xy_values(self.ZONES)[1][20] == 40


class TestAgreeablenessPerAgeGraph:

    def setup_method(self):
        script.Zone._initialize_zones()
        self.ZONE = script.Zone.ZONES[0]
        self.GRAPH = script.AgreeablenessPerAgeGraph()
        self.ZONES = script.Zone.ZONES
        for _ in range(0, 10):
            self.ZONE.add_inhabitant(script.Agent(script.Position(-180, -89), agreeableness=1, age=50))

    def test_title(self):
        assert self.GRAPH.title == 'Nice people are young'

    def test_x_label(self):
        assert self.GRAPH.x_label == 'age'

    def test_y_label(self):
        assert self.GRAPH.y_label == 'agreeableness'

    def test_xy_values(self):
        assert len(self.GRAPH.xy_values(self.ZONES)) == 2

    def test_age(self):
        assert self.GRAPH.xy_values(self.ZONES)[0][50] == 50

    def test_average_agreeableness_by_age(self):
        assert self.GRAPH.xy_values(self.ZONES)[1][50] == 1
