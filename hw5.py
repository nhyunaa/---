import mysql.connector


def connect_db():
    try:
        connection = mysql.connector.connect(
            host="192.168.56.103",
            user="rhyuna",
            password="1234",
            database="madang",
            port=4567
        )
        print("MySQL 서버 연결 성공!")
        return connection
    except mysql.connector.Error as err:
        print(f"데이터베이스 연결 에러: {err}")
        return None

# 데이터 삽입 
def insert_data(connection):
    cursor = connection.cursor()
    query = "INSERT INTO Book (bookid, bookname, publisher, price) VALUES (%s, %s, %s, %s)"
    
    try:
        #삽입하고자하는 책 ID가 table에 존재하는지에대한 쿼리문
        check_query = "SELECT COUNT(*) FROM Book WHERE bookid = %s"
        
        while True:
            # 사용자로부터 데이터 입력받기
            bookid = int(input("삽입할 책 ID (정수) : "))
            
           
            cursor.execute(check_query, (bookid,))
            count = cursor.fetchone()[0]
            
            #삽입하고자 하는 책 ID 가 table에 이미 존재하는경우 
            if count > 0:
                print(f"해당 책 ID {bookid} 존재, 다른 ID를 입력해주세요.")
                continue
            
            bookname = input("책이름 입력 : ")
            publisher = input("출판사 입력 : ")
            price = int(input("가격입력 (정수) : "))
            
            values = (bookid, bookname, publisher, price)
            
            cursor.execute(query, values)
            connection.commit()
            print("데이터 삽입 성공!")
            break
    except ValueError:
        print("입력 값이 올바르지 않습니다. 다시 시도해주세요.")
    except mysql.connector.Error as err:
        print(f"삽입 에러: {err}")
        connection.rollback()

# 데이터 삭제 
def delete_data(connection):
    cursor = connection.cursor()
    
    
    print("\n현재 Book 테이블 데이터:")
    search_data(connection)
    
    try:
        
        bookid = int(input("\n삭제할 책 ID 입력 : "))
        
        # 삭제 쿼리문
        query = "DELETE FROM Book WHERE bookid = %s"
        
      #삭제하고자하는 책이 테이블에 존재하는지 확인하는 쿼리문
        check_query = "SELECT COUNT(*) FROM Book WHERE bookid = %s"
        cursor.execute(check_query, (bookid,))
        count = cursor.fetchone()[0]
        
        if count == 0:
            print(f"책 ID {bookid}는 존재하지 않습니다.")
            return
        
        # 삭제 실행
        cursor.execute(query, (bookid,))
        connection.commit()
        print(f"책 ID {bookid}의 데이터 삭제 성공")
    except ValueError:
        print("정수 ID를 입력하십시오.")
    except mysql.connector.Error as err:
        print(f"삭제 에러: {err}")
        connection.rollback()

# 데이터 검색
def search_data(connection):
    cursor = connection.cursor()
    query = "SELECT * FROM Book ORDER BY bookid" 
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        if not rows:
            print("테이블에 데이터가 없습니다.")
            return
        print("검색 결과:")
        print("BookID | 책 이름 | 출판사 | 가격")
        print("-" * 50)
        for row in rows:
            print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]}")
    except mysql.connector.Error as err:
        print(f"검색 에러: {err}")

# 메인 함수
def main():
    connection = connect_db()
    if connection:
        try:
            while True:
                print("\n메뉴:")
                print("1. 데이터 삽입")
                print("2. 데이터 삭제")
                print("3. 데이터 검색")
                print("4. 종료")
                choice = input("선택 : ")

                if choice == "1":
                    insert_data(connection)
                elif choice == "2":
                    delete_data(connection)
                elif choice == "3":
                    search_data(connection)
                elif choice == "4":
                    print("프로그램을 종료합니다.")
                    break
                else:
                    print("잘못된 선택입니다. 다시 시도하세요.")
        finally:
            connection.close()

if __name__ == "__main__":
    main()