import csv
import os
import xml.etree.ElementTree as ET

contest_results = {}

def parse_file(input_file):
    tree = ET.parse(input_file)
    root = tree.getroot()

    timestamp = root.find('.//Timestamp').text
    electionName = root.find('.//ElectionName').text
    electionDate = root.find('.//ElectionDate').text
    region = root.find('.//Region').text

    precinctTotalVoters = {}
    precinctBallotsCast = {}
    precinctTurnoutPercent = {}

    for precinct in root.find('.//VoterTurnout/Precincts'):
        precinct_name = precinct.attrib['name']
        precinctTotalVoters[precinct_name] = precinct.attrib['totalVoters']
        precinctBallotsCast[precinct_name] = precinct.attrib['ballotsCast']
        precinctTurnoutPercent[precinct_name] = precinct.attrib['voterTurnout']

    for contest in root.findall('.//Contest'):
        contest_name = contest.attrib['text'] \
            .replace("/Presidentede los Estados Unidos", "") \
            .replace('/', '-')\
            .replace(',', ' ').strip()

        precinct_votes = {}

        for choice in contest.findall('.//Choice'):
            choice_name = choice.attrib['text'].replace(',', ' ')

            for vote_type in choice.findall('.//VoteType'):
                vote_type_name = vote_type.attrib['name']

                column = choice_name + "_" + vote_type_name

                for precinct in vote_type.findall('.//'):
                    precinct_name = precinct.attrib['name']
                    precinct_vote_count = precinct.attrib['votes']

                    precinct_votes.setdefault(
                        precinct_name,
                              {
                                '00_contest_name': contest_name,
                                '01_region': region,
                                '02_data_timestamp': timestamp,
                                '03_election_name': electionName,
                                '04_election_date': electionDate,
                               }
                    )

                    precinct_dict = precinct_votes[precinct_name]

                    precinct_dict['05_precinct_name'] = precinct_name
                    precinct_dict['06_precinct_total_voters'] = precinctTotalVoters[precinct_name]
                    precinct_dict['07_precinct_ballots_cast'] = precinctBallotsCast[precinct_name]
                    precinct_dict['08_precinct_turnout_%'] = precinctTurnoutPercent[precinct_name]
                    precinct_dict[column] = precinct_vote_count

        contest_results.setdefault(contest_name, [])

        for precinct_name, precinct_results in precinct_votes.items():
            contest_results[contest_name].append(precinct_results)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    for root, dir, files in os.walk('county-xml'):
        for file in files:
            filename = "county-xml/" + file
            print("Parsing", filename)
            parse_file(filename)

    for contest_name, precinct_results in contest_results.items():

        # Get the set of all headers for this contest
        headers = []
        for result in precinct_results:
            headers = sorted(list(set(headers) | set(result.keys())))

        with open('contest-csv/' + contest_name + ".csv", 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()

            for row in precinct_results:
                writer.writerow(row)
