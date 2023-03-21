-- adding new column into the table
ALTER TABLE players
ADD COLUMN AgeCategory TEXT

-- updating players table according to the condition
UPDATE players
 SET AgeCategory = CASE 
 WHEN age <= 23 THEN 'Young'
 WHEN age BETWEEN 24 AND 32 THEN 'MidAge'
 ELSE 'Old'
 END


-- calculate the average age, average number of appearances, and total number of players by club
SELECT 
 Current_Club AS club, 
 AVG(Age) AS avg_age, 
 AVG(Appearance) AS avg_appearances, 
 COUNT(Player_Id) AS total_players
FROM players
WHERE Current_Club IS NOT NULL
GROUP BY Current_Club;

-- choosing the club and extracting
SELECT p.name, COUNT(*) AS num_players
FROM players p
WHERE p.Current_Club = 'Liverpool'
AND EXISTS (
 SELECT 1
 FROM players p2
 WHERE p2.age < p.age
 AND p2.position = p.position
 AND p2.Appearance > p.Appearance
)
GROUP BY p.name;

-- selecting player from club
SELECT *
FROM players
WHERE current_club = 'Barcelona';

-- selecting player from position
SELECT *
FROM players
WHERE Position = 'Left-back';

