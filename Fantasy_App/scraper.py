import requests
from bs4 import BeautifulSoup

def get_premier_league_table():
    link = "https://onefootball.com/en/competition/premier-league-9/table"
    source = requests.get(link).text
    page = BeautifulSoup(source, "lxml")

    rows = page.find_all("li", class_="Standing_standings__row__5sdZG")

    table = []
    table.append(["Position", "Team", "Played", "Wins", "Draws", "Losses", "Goal Difference", "Points"])

    for row in rows:
        position_elem = row.find("div", class_="Standing_standings__cell__5Kd0W")
        team_elem = row.find("p", class_="Standing_standings__teamName__psv61")
        stats = row.find_all("div", class_="Standing_standings__cell__5Kd0W")

        if position_elem and team_elem and len(stats) >= 7:
            position = position_elem.text.strip()
            team = team_elem.text.strip()
            played = stats[2].text.strip()
            wins = stats[3].text.strip()
            draws = stats[4].text.strip()
            losses = stats[5].text.strip()
            goal_difference = stats[6].text.strip()
            points = stats[7].text.strip()

            table.append([position, team, played, wins, draws, losses, goal_difference, points])

    return table
