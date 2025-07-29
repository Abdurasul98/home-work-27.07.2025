import psycopg2

conn = psycopg2.connect(
    host='localhost',
    database='n68',
    user='n68',
    password='n68',
    port=5432
)

try:
    cur = conn.cursor()
    def drop_table_type():
        cur.execute("""
        DROP TABLE IF EXISTS salaries;
        DROP TYPE IF EXISTS VALID_SALARY_STATUS;
        """)
        conn.commit()


    def create_type():
        cur.execute("""
        CREATE TYPE VALID_SALARY_STATUS AS ENUM ('paid','pending','delayed');
        """)
        conn.commit()

    def create_table():
        cur.execute("""
        CREATE TABLE IF NOT EXISTS salaries (
            id SERIAL PRIMARY KEY,
            employee_name VARCHAR(128) NOT NULL,
            month DATE NOT NULL,
            base_salary NUMERIC NOT NULL,
            bonus NUMERIC DEFAULT 0,
            penalty NUMERIC DEFAULT 0,
            net_salary NUMERIC NOT NULL,
            STATUS VALID_SALARY_STATUS 
        );
        """)
        conn.commit()


    drop_table_type()
    create_type()
    create_table()

    def insertdata(employee_name: str, moth: str, base_salary: float, bonus: float, penalty: float, status: str):
        net_salary = base_salary + bonus - penalty

        cur.execute("""
        INSERT INTO salaries (employee_name, month, base_salary, bonus, penalty, net_salary, status)
        VALUES(%s,%s,%s,%s,%s,%s,%s);
        """, (employee_name, moth, base_salary, bonus, penalty, net_salary, status))
        conn.commit()

    insertdata('Ali Valiyev', '2025-07-01', 5000, 200, 50, 'pending')

    def selectNameMonth(employee_name:str = '',month:str = ''):
        cur.execute("""
        SELECT employee_name, month FROM salaries;
        """) , (employee_name,month)
        salaries = cur.fetchall()
        return salaries

    # data = selectNameMonth()
    # print(data)

    def selectMonth(user_month:str):
        cur.execute("""
                SELECT base_salary FROM salaries
                WHERE month = %s::date;
        """, (user_month,))
        salaries = cur.fetchall()
        return salaries

    # user_month = input("For example '9999-12-31': ")
    # data = selectMonth(user_month)
    # print(data)

    def selectStatus():
        cur.execute("""
                SELECT * FROM salaries
                WHERE status in ('pending', 'delayed');
        """)
        salaries = cur.fetchall()
        return salaries

    data = selectStatus()
    print(data)

    def updateStatus():
        cur.execute("""
        UPDATE salaries SET status = 'paid'
        WHERE status = 'pending' 
        """)
        conn.commit()


    updateStatus()

    def totalSalaryMonth():
        cur.execute("""
        SELECT SUM(net_salary) as total_base_salary FROM salaries
        WHERE status = 'paid'; 
        """)

        conn.commit()


    totalSalaryMonth()

    def bonus():
        cur.execute("""
        SELECT bonus , employee_name FROM salaries
        WHERE status = 'paid' 
        ORDER BY bonus DESC 
        LIMIT 1; 
        """)

        conn.commit()


    bonus()

    def penalty():
        cur.execute("""
        SELECT employee_name, penalty FROM salaries
        ORDER BY bonus DESC 
        LIMIT 1; 
        """)

        conn.commit()


    penalty()
except Exception as e:
    print(e)

finally:
    cur.close()
    conn.close()
