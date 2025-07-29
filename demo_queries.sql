-- ===========================
-- JOIN QUERIES
-- ===========================

-- 1. List all attendees for each event
SELECT EVENT_ID, EVENT_NAME, USER_ID, F_NAME, L_NAME
FROM (ATTENDED_BY NATURAL JOIN ATTENDEES NATURAL JOIN EVENTS);

-- 2. Get events that still have pending bills
SELECT DISTINCT EVENTS.EVENT_NAME
FROM BILLS
LEFT JOIN EVENTS ON BILLS.EVENT_ID = EVENTS.EVENT_ID
WHERE BILLS.PAYMENT_STATUS = 'Pending';

-- ===========================
-- AGGREGATE QUERIES
-- ===========================

-- 3. Total bill amount for a specific event
SELECT EVENTS.EVENT_NAME, SUM(BILLS.AMOUNT) AS TOTAL
FROM BILLS
LEFT JOIN EVENTS ON BILLS.EVENT_ID = EVENTS.EVENT_ID
WHERE EVENT_NAME = 'AatmaTrisha 2k22';

-- 4. Count attendees for each event
SELECT EVENTS.EVENT_NAME, COUNT(ATTENDED_BY.USER_ID) AS TOTAL_ATTENDEES
FROM ATTENDED_BY
LEFT JOIN EVENTS ON ATTENDED_BY.EVENT_ID = EVENTS.EVENT_ID
GROUP BY ATTENDED_BY.EVENT_ID;

-- 5. Event with the max attendees using CTE
WITH TEMP(NAME, TOTAL) AS (
  SELECT EVENTS.EVENT_NAME, COUNT(ATTENDED_BY.USER_ID) AS TOTAL_ATTENDEES
  FROM ATTENDED_BY
  LEFT JOIN EVENTS ON ATTENDED_BY.EVENT_ID = EVENTS.EVENT_ID
  GROUP BY ATTENDED_BY.EVENT_ID
)
SELECT NAME, MAX(TOTAL) FROM TEMP;

-- 6. Count suppliers in the 'Food' department
SELECT COUNT(DEPARTMENT) AS TOTAL
FROM SUPPLIER
WHERE SUPPLIER.DEPARTMENT = 'Food'
GROUP BY SUPPLIER.DEPARTMENT;

-- ===========================
-- SET OPERATIONS
-- ===========================

-- 7. Attendees in Karnataka OR first name starts with 'S'
SELECT ATTENDEES.F_NAME, ATTENDEES.L_NAME
FROM ATTENDEES 
WHERE ATTENDEES.STATE = 'Karnataka'
UNION
SELECT ATTENDEES.F_NAME, ATTENDEES.L_NAME
FROM ATTENDEES 
WHERE ATTENDEES.F_NAME LIKE 'S%';

-- 8. Events that have bills
SELECT DISTINCT EVENTS.EVENT_NAME
FROM EVENTS
INNER JOIN BILLS ON EVENTS.EVENT_ID = BILLS.EVENT_ID;

-- 9. Events that have no bills
SELECT EVENTS.EVENT_NAME 
FROM EVENTS 
WHERE EVENT_ID NOT IN (
    SELECT DISTINCT BILLS.EVENT_ID FROM BILLS
);

-- 10. Hosts that have events
SELECT DISTINCT EVENTS.HOST_ID, HOSTS.HOST_NAME 
FROM EVENTS 
INNER JOIN HOSTS 
ON EVENTS.HOST_ID = HOSTS.HOST_ID;

-- ===========================
-- FUNCTION DEMO
-- ===========================

-- 11. Use TOTAL_SALES() UDF (custom function) on attendees count table
SELECT EVENT_NAME, TOTAL_SALES(TABLE4.TOTAL_ATTENDEES) 
FROM TABLE4;

-- ===========================
-- PROCEDURE DEMO
-- ===========================

-- 12. Call stored procedure to return all bills (if implemented in DB)
CALL RETURN_ALL_BILLS();

-- ===========================
-- CURSOR & DELETE DEMO
-- ===========================

-- 13. Delete specific attendees (for cursor/delete demonstration)
DELETE FROM attendees WHERE `attendees`.`USER_ID` = 10;
DELETE FROM attendees WHERE `attendees`.`USER_ID` = 12;

-- 14. Call backup procedure (if implemented)
CALL BACKUP();
