import mysql.connector

# Database connection configuration
config = {
    "host": "mysql-2d50f4f1-xudoyberdiyevrahmatilla-b900.i.aivencloud.com",
    "port": 10187,
    "user": "avnadmin",
    "password": "AVNS_8pPnOCVBSgx4GU5dG3K",
    "database": "defaultdb",
} 

# Data to insert
regions = [
    "Toshkent", "Samarqand", "Andijon", "Farg'ona", "Namangan",
    "Buxoro", "Xorazm", "Navoiy", "Qashqadaryo", "Surxondaryo",
    "Jizzax", "Sirdaryo"
]

branches = {
    "Toshkent": ["Chilonzor filiali", "Yunusobod filiali", "Mirzo Ulug'bek filiali", "Sergeli filiali", "Bektemir filiali"],
    "Samarqand": ["Registon filiali", "Siyob bozori filiali", "Universitet filiali", "Afrosiyob filiali", "Go'ri Amir filiali"],
    "Andijon": ["Andijon shahar filiali", "Asaka filiali", "Xonobod filiali", "Shahrixon filiali", "Paxtaobod filiali"],
    "Farg'ona": ["Farg'ona shahar filiali", "Marg'ilon filiali", "Qo'qon filiali", "Rishton filiali", "Oltiariq filiali"],
    "Namangan": ["Namangan shahar filiali", "Chortoq filiali", "Uchqo'rg'on filiali", "Pop filiali", "To'raqo'rg'on filiali"]
}

courses = {
    "Chilonzor filiali": [
        "Dasturlash asoslari", "Veb-dasturlash", "Ma'lumotlar bazasi", "Sun'iy intellekt", "Kiberxavfsizlik"
    ],
    "Registon filiali": [
        "Grafik dizayn", "UX/UI dizayn", "Fotografiya", "3D Modellashtirish", "Video montaj"
    ],
    "Andijon shahar filiali": [
        "Mobil ilovalar yaratish", "Android dasturlash", "iOS dasturlash", "Flutter", "React Native"
    ],
    "Farg'ona shahar filiali": [
        "Biznes reja tuzish", "Startup menejmenti", "Moliyaviy savodxonlik", "Raqamli marketing", "Investitsiyalar"
    ],
    "Namangan shahar filiali": [
        "Ijtimoiy media marketing", "SEO optimizatsiya", "Google Ads", "SMM strategiya", "Kontent yaratish"
    ]
}

# Connect to the database
try:
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    # Insert regions and store their IDs
    region_ids = {}
    for region in regions:
        cursor.execute("INSERT INTO regions (name) VALUES (%s)", (region,))
        region_ids[region] = cursor.lastrowid
    
    # Insert branches and store their IDs
    branch_ids = {}
    for region, branch_list in branches.items():
        for branch in branch_list:
            cursor.execute("INSERT INTO branches (name, info, region_id) VALUES (%s, %s, %s)",
                           (branch, f"{branch} joylashuvi haqida ma'lumot", region_ids[region]))
            branch_ids[branch] = cursor.lastrowid
    
    # Insert courses
    for branch, course_list in courses.items():
        for course in course_list:
            cursor.execute("INSERT INTO courses (name, info, branch_id) VALUES (%s, %s, %s)",
                           (course, f"{course} kursi haqida batafsil ma'lumot", branch_ids[branch]))
    
    connection.commit()
    print("Sample data successfully inserted!")

except mysql.connector.Error as err:
    print(f"Error: {err}")

finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("Database connection closed.")