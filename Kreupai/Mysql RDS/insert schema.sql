create database kreupai;
use kreupai;

CREATE TABLE teamid (
    teamname VARCHAR(40) NOT NULL,
    teamid INT(5) PRIMARY KEY
);

CREATE TABLE matches (
    matchid     INT PRIMARY KEY,         
    matchname   VARCHAR(60) NOT NULL,    
    season      VARCHAR(9) NOT NULL,     
    match_dt    DATETIME NOT NULL      
);

CREATE TABLE matchresults (
    matchid        INT NOT NULL,
    teamid         INT NOT NULL,
    opponentid     INT NOT NULL,
    ishome         TINYINT(1) NOT NULL CHECK (ishome IN (0,1)), -- 0=away, 1=home
    goals_scored   INT(2) NOT NULL,
    goals_conceded INT(2) NOT NULL,
    result         VARCHAR(1) NOT NULL CHECK (result IN ('W','D','L')),
    PRIMARY KEY (matchid, teamid),    -- one row per team per match
    FOREIGN KEY (matchid)   REFERENCES matches(matchid)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (teamid)    REFERENCES teamid(teamid)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (opponentid)REFERENCES teamid(teamid)
        ON UPDATE CASCADE ON DELETE CASCADE
);


