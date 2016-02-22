import scrapy, random

from nfl.items import NFLTeam, Player

class NFLSpider(scrapy.Spider):
    name = "nflspider"
    allowed_domains = ["cbssports.com"]
    start_urls = [
        "http://cbssports.com/nfl/teams/stats/BUF/buffalo-bills",
        "http://cbssports.com/nfl/teams/stats/MIA/miami-dolphins",
        "http://cbssports.com/nfl/teams/stats/NE/new-england-patriots",
        "http://cbssports.com/nfl/teams/stats/NYJ/new-york-jets",
        "http://cbssports.com/nfl/teams/stats/BAL/baltimore-ravens",
        "http://cbssports.com/nfl/teams/stats/CIN/cincinnati-bengals",
        "http://cbssports.com/nfl/teams/stats/CLE/cleveland-browns",
        "http://cbssports.com/nfl/teams/stats/PIT/pittsburgh-steelers",
        "http://cbssports.com/nfl/teams/stats/HOU/houston-texans",
        "http://cbssports.com/nfl/teams/stats/IND/indianapolis-colts",
        "http://cbssports.com/nfl/teams/stats/JAC/jacksonville-jaguars",
        "http://cbssports.com/nfl/teams/stats/TEN/tennessee-titans",
        "http://cbssports.com/nfl/teams/stats/DEN/denver-broncos",
        "http://cbssports.com/nfl/teams/stats/KC/kansas-city-chiefs",
        "http://cbssports.com/nfl/teams/stats/OAK/oakland-raiders",
        "http://cbssports.com/nfl/teams/stats/SD/san-diego-chargers",
        "http://cbssports.com/nfl/teams/stats/DAL/dallas-cowboys",
        "http://cbssports.com/nfl/teams/stats/NYG/new-york-giants",
        "http://cbssports.com/nfl/teams/stats/PHI/philadelphia-eagles",
        "http://cbssports.com/nfl/teams/stats/WAS/washington-redskins",
        "http://cbssports.com/nfl/teams/stats/CHI/chicago-bears",
        "http://cbssports.com/nfl/teams/stats/DET/detroit-lions",
        "http://cbssports.com/nfl/teams/stats/GB/green-bay-packers",
        "http://cbssports.com/nfl/teams/stats/MIN/minnesota-vikings",
        "http://cbssports.com/nfl/teams/stats/ATL/atlanta-falcons",
        "http://cbssports.com/nfl/teams/stats/CAR/carolina-panthers",
        "http://cbssports.com/nfl/teams/stats/NO/new-orleans-saints",
        "http://cbssports.com/nfl/teams/stats/TB/tampa-bay-buccaneers ",
        "http://cbssports.com/nfl/teams/stats/ARI/arizona-cardinals",
        "http://cbssports.com/nfl/teams/stats/STL/st-louis-rams",
        "http://cbssports.com/nfl/teams/stats/SF/san-francisco-49ers",
        "http://cbssports.com/nfl/teams/stats/SEA/seattle-seahawks",
    ]

    def parse(self, response):
        nflteam = NFLTeam()
        temp = response.xpath('/html/head/title/text()').extract()
        temp = ''.join(temp)
        #temp = temp.split(' ')[0] + " " + temp.split(' ')[1]
        temp = temp.split('Stats')[0]
        temp = temp.strip()
        nflteam['teamname'] = temp
        #nflteam['roster'] = []
        nflteam['passers'] = []
        nflteam['rushers'] = []
        nflteam['receivers'] = []
        nflteam['sackers'] = []
        nflteam['passing_yards_leaders'] = []
        nflteam['rushing_yards_leaders'] = []
        nflteam['receive_yards_leaders'] = []
        nflteam['total_sacks_leaders'] = []

        #pull all passers on team
        max_rows = int(float(response.xpath('count(//table[2]/tr)').extract()[0])) - 5
        row_counter = 0
        rows = response.xpath('//table[2]/tr')
        category = rows.xpath('td/text()').extract()[0]

        while row_counter < max_rows:
            player = Player()
            tempname = rows.xpath('td/a/text()').extract()[row_counter]
            player['name'] = str(''.join(tempname).encode('utf-8')) 
            player['pass_yards'] = int(float(rows.xpath('td[8]/text()').extract()[row_counter]))
            nflteam['passers'].append(player)
            row_counter += 1

        #pull all passers on team
        max_rows = int(float(response.xpath('count(//table[3]/tr)').extract()[0])) - 5
        row_counter = 0
        rows = response.xpath('//table[3]/tr')
        category = rows.xpath('td/text()').extract()[0]

        while row_counter < max_rows:
            player = Player()
            tempname = rows.xpath('td/a/text()').extract()[row_counter]
            player['name'] = str(''.join(tempname).encode('utf-8'))
            player['rush_yards'] = int(float(rows.xpath('td[6]/text()').extract()[row_counter]))
            nflteam['rushers'].append(player)
            row_counter += 1
 
        #pull all receivers on team
        max_rows = int(float(response.xpath('count(//table[4]/tr)').extract()[0])) - 5
        row_counter = 0
        rows = response.xpath('//table[4]/tr')
        category = rows.xpath('td/text()').extract()[0]

        while row_counter < max_rows:
            player = Player()
            tempname = rows.xpath('td/a/text()').extract()[row_counter]
            player['name'] = str(''.join(tempname).encode('utf-8')) 
            player['receive_yards'] = int(float(rows.xpath('td[8]/text()').extract()[row_counter]))
            nflteam['receivers'].append(player)
            row_counter += 1
        
        #pull all sackers on team
        max_rows = int(float(response.xpath('count(//table[5]/tr)').extract()[0])) - 5
        row_counter = 0
        rows = response.xpath('//table[5]/tr')
        category = rows.xpath('td/text()').extract()[0]

        while row_counter < max_rows:
            player = Player()
            tempname = rows.xpath('td/a/text()').extract()[row_counter]
            player['name'] = str(''.join(tempname).encode('utf-8'))
            temp = float(rows.xpath('td[8]/text()').extract()[row_counter])
            if (temp != 0):
                player['total_sacks'] = temp
                nflteam['sackers'].append(player)
            row_counter += 1

        #sort sackers in descending order
        nflteam['sackers'] = sorted(nflteam['sackers'], key=lambda player: player['total_sacks'], reverse=True)

        #designate top four passers
        max_rows = len(nflteam['passers'])
        row_counter = 0
        while row_counter < max_rows:
            nflteam['passing_yards_leaders'].append(nflteam['passers'][row_counter]['name'])
            row_counter += 1
            if row_counter >= 4:
                break
        if max_rows < 4:
            index = len(nflteam['receivers'])
            while row_counter < 4:
                nflteam['passing_yards_leaders'].append(nflteam['receivers'][random.randint(0,index-1)]['name'])
                row_counter += 1
 
        #designate top four rushers
        max_rows = len(nflteam['rushers'])
        row_counter = 0
        while row_counter < max_rows:
            nflteam['rushing_yards_leaders'].append(nflteam['rushers'][row_counter]['name'])
            row_counter += 1
            if row_counter >= 4:
                break
        if max_rows < 4:
            index = len(nflteam['receivers'])
            while row_counter < 4:
                nflteam['rushing_yards_leaders'].append(nflteam['receivers'][random.randint(0,index-1)]['name'])
                row_counter += 1

        #designate top four receivers
        max_rows = len(nflteam['receivers'])
        row_counter = 0
        while row_counter < max_rows:
            nflteam['receive_yards_leaders'].append(nflteam['receivers'][row_counter]['name'])
            row_counter += 1
            if row_counter >= 4:
                break
        if max_rows < 4:
            index = len(nflteam['rushers'])
            while row_counter < 4:
                nflteam['receive_yards_leaders'].append(nflteam['rushers'][random.randint(0,index-1)]['name'])
                row_counter += 1

        #designate top four sackers
        max_rows = len(nflteam['sackers'])
        row_counter = 0
        while row_counter < max_rows:
            nflteam['total_sacks_leaders'].append(nflteam['sackers'][row_counter]['name'])
            row_counter += 1
            if row_counter >= 4:
                break
        if max_rows < 4:
            index = len(nflteam['receivers'])
            while row_counter < 4:
                nflteam['total_sacks_leaders'].append(nflteam['receivers'][random.randint(0,index-1)]['name'])
                row_counter += 1
 
        yield nflteam








