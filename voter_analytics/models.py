# voter_analytics/models.py
# Ting Shing Liu, 10/31/25
# Models for Voter Analytics app

from datetime import datetime
from django.db import models

class Voter(models.Model):
    """
    Represents a registered voter in Newton, MA.
    """
    # Personal & Address Info
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    street_number = models.IntegerField()
    street_name = models.CharField(max_length=200)
    apartment_number = models.CharField(max_length=20, blank=True, null=True)
    zip_code = models.CharField(max_length=10)
    
    # Voter Info
    date_of_birth = models.DateField()
    date_of_registration = models.DateField()
    party_affiliation = models.CharField(max_length=2)
    precinct_number = models.CharField(max_length=5)

    # Election Participation (Booleans)
    v20state = models.BooleanField(default=False)
    v21town = models.BooleanField(default=False)
    v21primary = models.BooleanField(default=False)
    v22general = models.BooleanField(default=False)
    v23town = models.BooleanField(default=False)
    
    # Summary Score
    voter_score = models.IntegerField()

    def __str__(self):
        """String representation of the Voter model."""
        return f"{self.first_name} {self.last_name} ({self.party_affiliation})"


def load_data():
    """
    Loads voter data from a CSV file into the Voter database.
    
    This function reads the file line-by-line and creates
    one object at a time, matching the marathon example style.
    """
    Voter.objects.all().delete()

    filename = r"\Users\victo\Downloads\newton_voters.csv"
    f = open(filename)
    f.readline()
    for line in f:
        fields = line.split(',')
       
        try:
            # create a new instance of Voter object with this record from CSV
            voter = Voter(
                last_name=fields[1],
                first_name=fields[2],
                street_number=int(fields[3]),
                street_name=fields[4],
                apartment_number=fields[5] if fields[5] else None,
                zip_code=fields[6],
                date_of_birth=datetime.strptime(fields[7], '%Y-%m-%d').date(),
                date_of_registration=datetime.strptime(fields[8], '%Y-%m-%d').date(),
                party_affiliation=fields[9].strip(),
                precinct_number=fields[10],
                v20state=fields[11].strip().upper() == 'TRUE',
                v21town=fields[12].strip().upper() == 'TRUE',
                v21primary=fields[13].strip().upper() == 'TRUE',
                v22general=fields[14].strip().upper() == 'TRUE',
                v23town=fields[15].strip().upper() == 'TRUE',
                voter_score=int(fields[16])
            )
            voter.save() # Commit this one voter to the database
        except Exception as e:
            print(f"--- Skipped line due to error: {e} ---")
            print(f"--- Offending data: {line} ---")
    f.close()