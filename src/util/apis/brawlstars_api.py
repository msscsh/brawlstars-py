import os, sys, json, requests

project_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_path)
from util.logger import log_line, log_line_in_debug

def add_banned_url_to_file(tag):
    file_path = 'banned_url.log'

    if not os.path.exists(file_path):
        with open(file_path, 'w') as novo_arquivo:
            pass

    with open(file_path, 'a') as hunted_file:
        hunted_file.write(f'{tag}\n')

def clean_columns_from_json(json_from_api, to_remove):
	json_less = {key: value for key, value in json_from_api.items() if key not in to_remove}
	return json_less

def do_request_for_list(url, list_name):
	json = do_request(url)
	json_final = {list_name: json['items']}
	return json_final

def manipulate_json_before_return(json_data):
    if isinstance(json_data, list):
        if all(isinstance(item, dict) for item in json_data):
            log_line_in_debug("List of Dictionaries")
        else:
            log_line_in_debug("List with elements of different types")
    elif isinstance(json_data, dict):
        log_line_in_debug("Single Dictionary")
        clean_columns_from_json(json_data, ["paging"])
    else:
        log_line_in_debug("Unknown Type")
    return json_data;

def do_request(url):
	with open('api_key', 'r') as arquivo:
	    api_key = arquivo.read()
	    headers = {
	        'Authorization': f'Bearer {api_key}'
	    }
	    response = requests.get(url, headers=headers)
	    if response.status_code == 200:
	    	return manipulate_json_before_return(response.json())
	    if response.status_code == 404:
	    	log_line(f'Error: 404 Not Found {url}')
	    	add_banned_url_to_file(url)
	    	return None
	    else:
	    	log_line(f'Error: {response.status_code} headers: {response.headers}')
	    	return None

def get_api_players_data(tag):
	url = f'{base_url_players}{tag}'
	json = do_request(url)
	json['tag'] = tag
	return clean_columns_from_json(json, ["brawlers", "club"])

def get_api_players_battlelog_data(tag):
	url = f'{base_url_players}{tag}/battlelog'
	json = do_request_for_list(url, 'battles')
	json = {"tag": tag, **json}
	return json

def get_api_players_battlelog_data_with_name(tag):
    player = get_api_players_data(tag)
    api_player_battlelog = get_api_players_battlelog_data(tag)
    api_player_battlelog = {'name': player['name'], **api_player_battlelog}
    return api_player_battlelog

def get_api_clubs(tag):
	url = f'{base_url_clubs}{tag}'
	json = do_request(url)
	json['tag'] = tag
	return clean_columns_from_json(json, ["members"])

def get_api_clubs_members(tag):
	url = f'{base_url_clubs}{tag}/members'
	json = do_request_for_list(url, 'members')
	json = {"tag": tag, **json}
	return json

def get_api_rankings_countrycode_powerplay_seasons(country_code):
	url = f'{base_url_rankings}/{country_code}/powerplay/seasons'
	json = do_request_for_list(url, 'pl_seasons')
	json = {"country_code": country_code, **json}
	return json

def get_api_rankings_countrycode_powerplay_seasons_seasonsid(country_code, seasonid):
	url = f'{base_url_rankings}/{country_code}/powerplay/seasons/{seasonid}'
	json = do_request_for_list(url, 'pl_seasons_ranking')
	json = {"country_code": country_code, **json}
	json = {"seasonid": seasonid, **json}
	return json

def get_api_rankings_countrycode_clubs(country_code):
	url = f'{base_url_rankings}/{country_code}/clubs'
	json = do_request_for_list(url, 'clubs_ranking')
	json = {"country_code": country_code, **json}
	return json

def get_api_rankings_countrycode_brawler_brawlerid(country_code, brawlersid):
	url = f'{base_url_rankings}/{country_code}/brawlers/{brawlersid}'
	json = do_request_for_list(url, 'brawlers_ranking')
	json = {"country_code": country_code, **json}
	json = {"brawlersid": brawlersid, **json}
	return json

def get_api_rankings_countrycode_players(country_code):
	url = f'{base_url_rankings}/{country_code}/players'
	json = do_request_for_list(url, 'players_ranking')
	json = {"country_code": country_code, **json}
	return json

def get_api_brawlers():
	url = f'{base_url_brawlers}'
	json = do_request_for_list(url, 'brawlers')
	return json

def get_api_brawler_brawlerid(brawler_id):
	url = f'{base_url_brawlers}/{brawler_id}'
	return do_request(url)

def get_api_events_rotation():
	url = f'{base_url_events}'
	return do_request(url)

def main(tag):
	# json_less = get_api_players_data(tag)
	# json_less = get_api_players_battlelog_data(tag)

	# json_less = get_api_clubs(tag)
	json_less = get_api_clubs_members(tag)

	# json_less = get_api_rankings_countrycode_powerplay_seasons('global')
	# json_less = get_api_rankings_countrycode_powerplay_seasons_seasonsid('global', 57)
	# json_less = get_api_rankings_countrycode_clubs('global')
	# json_less = get_api_rankings_countrycode_brawler_brawlerid('global', 16000000)
	# json_less = get_api_rankings_countrycode_players('global')

	# json_less = get_api_brawlers()
	# json_less = get_api_brawler_brawlerid(16000000)

	# json_less = get_api_events_rotation()

	print(json.dumps(json_less, indent=2, ensure_ascii=False))


base_url='https://api.brawlstars.com/v1'
base_url_players=f'{base_url}/players/%23'
base_url_clubs=f'{base_url}/clubs/%23'
base_url_brawlers=f'{base_url}/brawlers'
base_url_rankings=f'{base_url}/rankings'
base_url_events=f'{base_url}/events/rotation'

if __name__ == "__main__":
	if len(sys.argv) < 2:
		log_line("Directed started API module with no TAG informed")
		quit()
	else:
	    main(sys.argv[1])