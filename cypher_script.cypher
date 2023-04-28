:begin
CREATE CONSTRAINT UNIQUE_IMPORT_NAME FOR (node:`UNIQUE IMPORT LABEL`) REQUIRE (node.`UNIQUE IMPORT ID`) IS UNIQUE;
:commit
CALL db.awaitIndexes(300);
:begin
UNWIND [{_id:0, properties:{name:"Reepicheep", description:"Small, a mouse with a sword"}}, {_id:1, properties:{name:"Tumnus", description:"A faun."}}, {_id:5, properties:{name:"Lucy", description:"Youngest of the Pevensies. Discovers Narnia accidentally."}}, {_id:6, properties:{name:"Edmund", description:"Betrays Lucy for candy. Later becomes a follower of Aslan."}}, {_id:7, properties:{name:"Aslan", description:"The creator and ruler of Narnia. "}}, {_id:8, properties:{name:"Caspian", description:"Prince of Narnia"}}, {_id:10, properties:{name:"Peter", description:"Eldest Pevensie, High King of Narnia"}}, {_id:17, properties:{name:"White Witch", description:"Evil ruler of Narnia"}}, {_id:19, properties:{name:"Digory", description:"Witnesses the creation of Narnia"}}] AS row
CREATE (n:`UNIQUE IMPORT LABEL`{`UNIQUE IMPORT ID`: row._id}) SET n += row.properties SET n:Character;
UNWIND [{_id:11, properties:{name:"Wardrobe", description:"Made from the wood of an apple tree; portal from Earth to Narnia."}}, {_id:21, properties:{name:"Golden Apple", description:"Grants eternal life to whoever eats it."}}] AS row
CREATE (n:`UNIQUE IMPORT LABEL`{`UNIQUE IMPORT ID`: row._id}) SET n += row.properties SET n:Thing;
UNWIND [{_id:14, properties:{name:"Narnia", description:"The country rescued by Aslan from the White Witch. "}}, {_id:15, properties:{name:"Calormen", description:"A neighboring country to the southeast."}}] AS row
CREATE (n:`UNIQUE IMPORT LABEL`{`UNIQUE IMPORT ID`: row._id}) SET n += row.properties SET n:Place;
:commit
:begin
UNWIND [{start: {_id:1}, end: {_id:17}, properties:{}}] AS row
MATCH (start:`UNIQUE IMPORT LABEL`{`UNIQUE IMPORT ID`: row.start._id})
MATCH (end:`UNIQUE IMPORT LABEL`{`UNIQUE IMPORT ID`: row.end._id})
CREATE (start)-[r:FEARS]->(end) SET r += row.properties;
UNWIND [{start: {_id:17}, end: {_id:14}, properties:{}}] AS row
MATCH (start:`UNIQUE IMPORT LABEL`{`UNIQUE IMPORT ID`: row.start._id})
MATCH (end:`UNIQUE IMPORT LABEL`{`UNIQUE IMPORT ID`: row.end._id})
CREATE (start)-[r:RULER_OF]->(end) SET r += row.properties;
UNWIND [{start: {_id:21}, end: {_id:14}, properties:{}}] AS row
MATCH (start:`UNIQUE IMPORT LABEL`{`UNIQUE IMPORT ID`: row.start._id})
MATCH (end:`UNIQUE IMPORT LABEL`{`UNIQUE IMPORT ID`: row.end._id})
CREATE (start)-[r:HELPS_CREATE]->(end) SET r += row.properties;
UNWIND [{start: {_id:14}, end: {_id:11}, properties:{}}] AS row
MATCH (start:`UNIQUE IMPORT LABEL`{`UNIQUE IMPORT ID`: row.start._id})
MATCH (end:`UNIQUE IMPORT LABEL`{`UNIQUE IMPORT ID`: row.end._id})
CREATE (start)-[r:PORTAL]->(end) SET r += row.properties;
UNWIND [{start: {_id:15}, end: {_id:8}, properties:{}}] AS row
MATCH (start:`UNIQUE IMPORT LABEL`{`UNIQUE IMPORT ID`: row.start._id})
MATCH (end:`UNIQUE IMPORT LABEL`{`UNIQUE IMPORT ID`: row.end._id})
CREATE (start)-[r:HOMELAND_OF]->(end) SET r += row.properties;
UNWIND [{start: {_id:11}, end: {_id:5}, properties:{}}] AS row
MATCH (start:`UNIQUE IMPORT LABEL`{`UNIQUE IMPORT ID`: row.start._id})
MATCH (end:`UNIQUE IMPORT LABEL`{`UNIQUE IMPORT ID`: row.end._id})
CREATE (start)-[r:ENTERED_BY]->(end) SET r += row.properties;
UNWIND [{start: {_id:6}, end: {_id:5}, properties:{}}, {start: {_id:10}, end: {_id:5}, properties:{}}, {start: {_id:10}, end: {_id:6}, properties:{}}] AS row
MATCH (start:`UNIQUE IMPORT LABEL`{`UNIQUE IMPORT ID`: row.start._id})
MATCH (end:`UNIQUE IMPORT LABEL`{`UNIQUE IMPORT ID`: row.end._id})
CREATE (start)-[r:SIBLING]->(end) SET r += row.properties;
UNWIND [{start: {_id:1}, end: {_id:5}, properties:{}}] AS row
MATCH (start:`UNIQUE IMPORT LABEL`{`UNIQUE IMPORT ID`: row.start._id})
MATCH (end:`UNIQUE IMPORT LABEL`{`UNIQUE IMPORT ID`: row.end._id})
CREATE (start)-[r:MEETS]->(end) SET r += row.properties;
UNWIND [{start: {_id:19}, end: {_id:11}, properties:{}}] AS row
MATCH (start:`UNIQUE IMPORT LABEL`{`UNIQUE IMPORT ID`: row.start._id})
MATCH (end:`UNIQUE IMPORT LABEL`{`UNIQUE IMPORT ID`: row.end._id})
CREATE (start)-[r:BUILDS]->(end) SET r += row.properties;
UNWIND [{start: {_id:14}, end: {_id:10}, properties:{}}, {start: {_id:14}, end: {_id:8}, properties:{}}] AS row
MATCH (start:`UNIQUE IMPORT LABEL`{`UNIQUE IMPORT ID`: row.start._id})
MATCH (end:`UNIQUE IMPORT LABEL`{`UNIQUE IMPORT ID`: row.end._id})
CREATE (start)-[r:RULED_BY]->(end) SET r += row.properties;
UNWIND [{start: {_id:15}, end: {_id:14}, properties:{}}] AS row
MATCH (start:`UNIQUE IMPORT LABEL`{`UNIQUE IMPORT ID`: row.start._id})
MATCH (end:`UNIQUE IMPORT LABEL`{`UNIQUE IMPORT ID`: row.end._id})
CREATE (start)-[r:BORDERS]->(end) SET r += row.properties;
UNWIND [{start: {_id:17}, end: {_id:7}, properties:{}}] AS row
MATCH (start:`UNIQUE IMPORT LABEL`{`UNIQUE IMPORT ID`: row.start._id})
MATCH (end:`UNIQUE IMPORT LABEL`{`UNIQUE IMPORT ID`: row.end._id})
CREATE (start)-[r:CRUCIFIES]->(end) SET r += row.properties;
UNWIND [{start: {_id:7}, end: {_id:6}, properties:{}}] AS row
MATCH (start:`UNIQUE IMPORT LABEL`{`UNIQUE IMPORT ID`: row.start._id})
MATCH (end:`UNIQUE IMPORT LABEL`{`UNIQUE IMPORT ID`: row.end._id})
CREATE (start)-[r:DIES_FOR]->(end) SET r += row.properties;
UNWIND [{start: {_id:10}, end: {_id:8}, properties:{}}] AS row
MATCH (start:`UNIQUE IMPORT LABEL`{`UNIQUE IMPORT ID`: row.start._id})
MATCH (end:`UNIQUE IMPORT LABEL`{`UNIQUE IMPORT ID`: row.end._id})
CREATE (start)-[r:FIGHTS_ALONG]->(end) SET r += row.properties;
UNWIND [{start: {_id:0}, end: {_id:8}, properties:{}}] AS row
MATCH (start:`UNIQUE IMPORT LABEL`{`UNIQUE IMPORT ID`: row.start._id})
MATCH (end:`UNIQUE IMPORT LABEL`{`UNIQUE IMPORT ID`: row.end._id})
CREATE (start)-[r:FRIEND_OF]->(end) SET r += row.properties;
UNWIND [{start: {_id:17}, end: {_id:6}, properties:{}}] AS row
MATCH (start:`UNIQUE IMPORT LABEL`{`UNIQUE IMPORT ID`: row.start._id})
MATCH (end:`UNIQUE IMPORT LABEL`{`UNIQUE IMPORT ID`: row.end._id})
CREATE (start)-[r:CAPTURES]->(end) SET r += row.properties;
:commit
:begin
MATCH (n:`UNIQUE IMPORT LABEL`)  WITH n LIMIT 20000 REMOVE n:`UNIQUE IMPORT LABEL` REMOVE n.`UNIQUE IMPORT ID`;
:commit
:begin
DROP CONSTRAINT UNIQUE_IMPORT_NAME;
:commit