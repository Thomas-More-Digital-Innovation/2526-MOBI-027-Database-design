import csv
import re

import mysql.connector
from mysql.connector import Error

import os
from dotenv import load_dotenv

load_dotenv()

# Database configuration
db_config = {
     'host': os.getenv('DB_HOST'),
     'user': os.getenv('DB_USER'),
     'password': os.getenv('DB_PASSWORD'),
     'database': os.getenv('DB_NAME'),
     'port': int(os.getenv('DB_PORT'))
 }

# CSV file paths - update these to match your file locations
CSV_FILES = {
    'part1': 'neo4j_query_table_data_2025-10-15.csv',
    'part2': 'neo4j_query_table_data_2025-10-15(2).csv',
    'part3': 'neo4j_query_table_data_2025-10-15(3).csv',  
    'part4': 'neo4j_query_table_data_2025-10-16.csv',
    'part5': 'neo4j_query_table_data_2025-10-16(2).csv',
    'part6': 'neo4j_query_table_data_2025-10-22.csv',
}

def parse_node(node_str):
    """Parse a Cypher-style node string into a dictionary"""
    if not node_str or node_str == '':
        return None
    
    match = re.match(r'\(:(\w+)\s*{(.+)}\)', node_str)
    if not match:
        return None
    
    node_type = match.group(1)
    props_str = match.group(2)
    
    props = {}
    parts = re.findall(r'(\w+):\s*([^,}]+?)(?:,|$)', props_str)
    
    for key, value in parts:
        value = value.strip()
        if value.startswith('"') and value.endswith('"'):
            value = value[1:-1]
        props[key] = value
    
    return {'type': node_type, 'properties': props}

def parse_relationship(rel_str):
    """Parse a Cypher-style relationship string into a dictionary"""
    if not rel_str or rel_str == '':
        return None
    
    match = re.match(r'\[:(\w+)(?:\s*{(.+)})?\]', rel_str)
    if not match:
        return None
    
    rel_type = match.group(1)
    props_str = match.group(2)
    
    props = {}
    if props_str:
        parts = re.findall(r'(\w+):\s*([^,}]+?)(?:,|$)', props_str)
        
        for key, value in parts:
            value = value.strip()
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            props[key] = value
    
    return {'type': rel_type, 'properties': props}

def connect_db():
    """Create database connection"""
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            print("Successfully connected to MySQL database")
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

# ====================
# INSERT FUNCTIONS
# ====================

def insert_exo(cursor, exo_data, update_mode=True):
    """Insert or update Exo record"""
    if update_mode:
        query = """
        INSERT INTO Exo (exoId, exoName, exoManufacturer, exoDescription, 
                         exoMaterial, exoOneTwoSided, exoActivePassive)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            exoName = VALUES(exoName),
            exoManufacturer = VALUES(exoManufacturer),
            exoDescription = VALUES(exoDescription),
            exoMaterial = VALUES(exoMaterial),
            exoOneTwoSided = VALUES(exoOneTwoSided),
            exoActivePassive = VALUES(exoActivePassive)
        """
    else:
        query = """
        INSERT INTO Exo (exoId, exoName, exoManufacturer, exoDescription, 
                         exoMaterial, exoOneTwoSided, exoActivePassive)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE exoId = exoId
        """
    
    props = exo_data['properties']
    values = (
        int(props.get('exoId', 0)),
        props.get('exoName', ''),
        props.get('exoManufacturer', ''),
        props.get('exoDescription', ''),
        props.get('exoMaterial', ''),
        props.get('exoOneTwoSided', ''),
        props.get('exoActivePassive', '')
    )
    
    cursor.execute(query, values)
    return int(props.get('exoId', 0))

def insert_aim(cursor, aim_data, update_mode=True):
    """Insert or update Aim record"""
    if update_mode:
        query = """
        INSERT INTO Aim (aimId, aimName, aimNameEn, aimDescription, aimIsSelectable)
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            aimName = VALUES(aimName),
            aimNameEn = VALUES(aimNameEn),
            aimDescription = VALUES(aimDescription),
            aimIsSelectable = VALUES(aimIsSelectable)
        """
    else:
        query = """
        INSERT INTO Aim (aimId, aimName, aimNameEn, aimDescription, aimIsSelectable)
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE aimId = aimId
        """
    
    props = aim_data['properties']
    values = (
        int(props.get('aimId', 0)),
        props.get('aimName', ''),
        props.get('aimNameEn', ''),
        props.get('aimDescription', ''),
        props.get('aimIsSelectable', '')
    )
    
    cursor.execute(query, values)
    return int(props.get('aimId', 0))

def insert_structure_kinematic_name(cursor, skn_data, update_mode=True):
    """Insert or update StructureKinematicName record"""
    if update_mode:
        query = """
        INSERT INTO StructureKinematicName (structureKinematicNameId, structureKinematicNameName, 
                                             structureKinematicNameNameEn, structureKinematicNameIsSelectable)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            structureKinematicNameName = VALUES(structureKinematicNameName),
            structureKinematicNameNameEn = VALUES(structureKinematicNameNameEn),
            structureKinematicNameIsSelectable = VALUES(structureKinematicNameIsSelectable)
        """
    else:
        query = """
        INSERT INTO StructureKinematicName (structureKinematicNameId, structureKinematicNameName, 
                                             structureKinematicNameNameEn, structureKinematicNameIsSelectable)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE structureKinematicNameId = structureKinematicNameId
        """
    
    props = skn_data['properties']
    values = (
        int(props.get('structureKinematicNameId', 0)),
        props.get('structureKinematicNameName', ''),
        props.get('structureKinematicNameNameEn', ''),
        props.get('structureKinematicNameIsSelectable', '')
    )
    
    cursor.execute(query, values)
    return int(props.get('structureKinematicNameId', 0))

def get_or_create_property(cursor, property_name):
    """Get or create ExoProperty and return its ID"""
    cursor.execute("SELECT exoPropertyId FROM ExoProperty WHERE exoPropertyName = %s", (property_name,))
    result = cursor.fetchone()
    
    if result:
        return result[0]
    
    cursor.execute("INSERT INTO ExoProperty (exoPropertyName) VALUES (%s)", (property_name,))
    return cursor.lastrowid

def insert_dof(cursor, dof_data, update_mode=True):
    """Insert or update Dof record"""
    if update_mode:
        query = """
        INSERT INTO Dof (dofId, dofName, namePos, nameNeg, dofDirection)
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            dofName = VALUES(dofName),
            namePos = VALUES(namePos),
            nameNeg = VALUES(nameNeg),
            dofDirection = VALUES(dofDirection)
        """
    else:
        query = """
        INSERT INTO Dof (dofId, dofName, namePos, nameNeg, dofDirection)
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE dofId = dofId
        """
    
    props = dof_data['properties']
    values = (
        int(props.get('dofId', 0)),
        props.get('dofName', ''),
        props.get('namePos', ''),
        props.get('nameNeg', ''),
        props.get('dofDirection', '')
    )
    
    cursor.execute(query, values)
    return int(props.get('dofId', 0))

def insert_joint_t(cursor, joint_data, update_mode=True):
    """Insert or update JointT record"""
    if update_mode:
        query = """
        INSERT INTO JointT (jointTId, jointTName)
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE jointTName = VALUES(jointTName)
        """
    else:
        query = """
        INSERT INTO JointT (jointTId, jointTName)
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE jointTId = jointTId
        """
    
    props = joint_data['properties']
    values = (
        int(props.get('jointTId', 0)),
        props.get('jointTName', '')
    )
    
    cursor.execute(query, values)
    return int(props.get('jointTId', 0))

def insert_part(cursor, part_data, update_mode=True):
    """Insert or update Part record"""
    if update_mode:
        query = """
        INSERT INTO Part (partId, partName, partType)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE
            partName = VALUES(partName),
            partType = VALUES(partType)
        """
    else:
        query = """
        INSERT INTO Part (partId, partName, partType)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE partId = partId
        """
    
    props = part_data['properties']
    values = (
        int(props.get('partId', 0)),
        props.get('partName', ''),
        props.get('partType', '')
    )
    
    cursor.execute(query, values)
    return int(props.get('partId', 0))

def get_or_create_aimtype(cursor, aimtype_data):
    """Get or create AimType and return its ID"""
    props = aimtype_data['properties']
    aim_type_name = props.get('aimTypeName', '')
    
    cursor.execute("SELECT aimTypeId FROM AimType WHERE aimTypeName = %s", (aim_type_name,))
    result = cursor.fetchone()
    
    if result:
        return result[0]
    
    query = """
    INSERT INTO AimType (aimTypeName, aimTypeNameEn, aimTypeIsSelectable)
    VALUES (%s, %s, %s)
    """
    values = (
        aim_type_name,
        props.get('aimTypeNameEn', ''),
        props.get('aimTypeIsSelectable', '')
    )
    cursor.execute(query, values)
    return cursor.lastrowid

def get_or_create_structure_kinematic_name_type(cursor, skntype_data):
    """Get or create StructureKinematicNameType and return its ID"""
    props = skntype_data['properties']
    skn_type_name = props.get('structureKinematicNameTypeName', '')
    
    cursor.execute("SELECT structureKinematicNameTypeId FROM StructureKinematicNameType WHERE structureKinematicNameTypeName = %s", (skn_type_name,))
    result = cursor.fetchone()
    
    if result:
        return result[0]
    
    query = """
    INSERT INTO StructureKinematicNameType (structureKinematicNameTypeName, structureKinematicNameTypeNameEn, structureKinematicNameTypeIsSelectable)
    VALUES (%s, %s, %s)
    """
    values = (
        skn_type_name,
        props.get('structureKinematicNameTypeNameEn', ''),
        props.get('structureKinematicNameTypeIsSelectable', '')
    )
    cursor.execute(query, values)
    return cursor.lastrowid

# ====================
# RELATIONSHIP FUNCTIONS
# ====================

def insert_has_aim(cursor, exo_id, aim_id, aim_category):
    """Insert HAS_AIM relationship"""
    query = """
    INSERT IGNORE INTO HAS_AIM (exoId, aimId, aimCategory)
    VALUES (%s, %s, %s)
    """
    cursor.execute(query, (exo_id, aim_id, aim_category))

def insert_has_aim_structure(cursor, exo_id, structure_id, category):
    """Insert HAS_AIM_Structure relationship"""
    query = """
    INSERT IGNORE INTO HAS_AIM_Structure (exoId, structureKinematicNameId, structureKinematicNameCategory)
    VALUES (%s, %s, %s)
    """
    cursor.execute(query, (exo_id, structure_id, category))

def insert_has_property(cursor, exo_id, property_id, property_value):
    """Insert HAS_PROPERTY relationship"""
    query = """
    INSERT INTO HAS_PROPERTY (exoId, exoPropertyId, exoPropertyValue)
    VALUES (%s, %s, %s)
    ON DUPLICATE KEY UPDATE exoPropertyValue = VALUES(exoPropertyValue)
    """
    cursor.execute(query, (exo_id, property_id, property_value))

def insert_assists_in(cursor, exo_id, dof_id, rel_props):
    """Insert ASSISTS_IN relationship"""
    query = """
    INSERT INTO ASSISTS_IN (exoId, dofId, aim, direction, rangeAdjustable, 
                            sizeAdjustable, lowerBoundMinAngle, lowerBoundMaxAngle,
                            upperBoundMinAngle, upperBoundMaxAngle)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        aim = VALUES(aim),
        direction = VALUES(direction),
        rangeAdjustable = VALUES(rangeAdjustable),
        sizeAdjustable = VALUES(sizeAdjustable),
        lowerBoundMinAngle = VALUES(lowerBoundMinAngle),
        lowerBoundMaxAngle = VALUES(lowerBoundMaxAngle),
        upperBoundMinAngle = VALUES(upperBoundMinAngle),
        upperBoundMaxAngle = VALUES(upperBoundMaxAngle)
    """
    
    values = (
        exo_id,
        dof_id,
        rel_props.get('aim'),
        int(rel_props.get('direction', 0)) if rel_props.get('direction') else None,
        rel_props.get('rangeAdjustable'),
        rel_props.get('sizeAdjustable'),
        int(rel_props.get('lowerBoundMinAngle', 0)) if rel_props.get('lowerBoundMinAngle') else None,
        int(rel_props.get('lowerBoundMaxAngle', 0)) if rel_props.get('lowerBoundMaxAngle') else None,
        int(rel_props.get('upperBoundMinAngle', 0)) if rel_props.get('upperBoundMinAngle') else None,
        int(rel_props.get('upperBoundMaxAngle', 0)) if rel_props.get('upperBoundMaxAngle') else None
    )
    
    cursor.execute(query, values)

def insert_has_dof(cursor, joint_id, dof_id):
    """Insert HAS_DOF relationship"""
    query = """
    INSERT IGNORE INTO HAS_DOF (jointTId, dofId)
    VALUES (%s, %s)
    """
    cursor.execute(query, (joint_id, dof_id))

def insert_doesnt_go_with(cursor, exo_id, structure_id):
    """Insert DOESNT_GO_WITH relationship"""
    query = """
    INSERT IGNORE INTO DOESNT_GO_WITH (exoId, structureKinematicNameId)
    VALUES (%s, %s)
    """
    cursor.execute(query, (exo_id, structure_id))

def insert_has_as_main_dof(cursor, exo_id, dof_id):
    """Insert HAS_AS_MAIN_DOF relationship"""
    query = """
    INSERT IGNORE INTO HAS_AS_MAIN_DOF (exoId, dofId)
    VALUES (%s, %s)
    """
    cursor.execute(query, (exo_id, dof_id))

def insert_gives_resistance_in(cursor, exo_id, dof_id, rel_props):
    """Insert GIVES_RESISTANCE_IN relationship"""
    query = """
    INSERT INTO GIVES_RESISTANCE_IN (exoId, dofId, aim, direction, rangeAdjustable, 
                                      sizeAdjustable, lowerBoundMinAngle, lowerBoundMaxAngle,
                                      upperBoundMinAngle, upperBoundMaxAngle)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        aim = VALUES(aim),
        direction = VALUES(direction),
        rangeAdjustable = VALUES(rangeAdjustable),
        sizeAdjustable = VALUES(sizeAdjustable),
        lowerBoundMinAngle = VALUES(lowerBoundMinAngle),
        lowerBoundMaxAngle = VALUES(lowerBoundMaxAngle),
        upperBoundMinAngle = VALUES(upperBoundMinAngle),
        upperBoundMaxAngle = VALUES(upperBoundMaxAngle)
    """
    
    values = (
        exo_id,
        dof_id,
        rel_props.get('aim'),
        int(rel_props.get('direction', 0)) if rel_props.get('direction') else None,
        rel_props.get('rangeAdjustable'),
        rel_props.get('sizeAdjustable'),
        int(rel_props.get('lowerBoundMinAngle', 0)) if rel_props.get('lowerBoundMinAngle') else None,
        int(rel_props.get('lowerBoundMaxAngle', 0)) if rel_props.get('lowerBoundMaxAngle') else None,
        int(rel_props.get('upperBoundMinAngle', 0)) if rel_props.get('upperBoundMinAngle') else None,
        int(rel_props.get('upperBoundMaxAngle', 0)) if rel_props.get('upperBoundMaxAngle') else None
    )
    
    cursor.execute(query, values)

def insert_gives_postural_support_in(cursor, exo_id, dof_id, rel_props):
    """Insert GIVES_POSTURAL_SUPPORT_IN relationship"""
    query = """
    INSERT INTO GIVES_POSTURAL_SUPPORT_IN (exoId, dofId, aim, direction, adjustable, 
                                         mechanism, rangeAdjustable, sizeAdjustable,
                                         minAngle, maxAngle,
                                         lowerBoundMinAngle, lowerBoundMaxAngle,
                                         upperBoundMinAngle, upperBoundMaxAngle)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        aim = VALUES(aim),
        direction = VALUES(direction),
        adjustable = VALUES(adjustable),
        mechanism = VALUES(mechanism),
        rangeAdjustable = VALUES(rangeAdjustable),
        sizeAdjustable = VALUES(sizeAdjustable),
        minAngle = VALUES(minAngle),
        maxAngle = VALUES(maxAngle),
        lowerBoundMinAngle = VALUES(lowerBoundMinAngle),
        lowerBoundMaxAngle = VALUES(lowerBoundMaxAngle),
        upperBoundMinAngle = VALUES(upperBoundMinAngle),
        upperBoundMaxAngle = VALUES(upperBoundMaxAngle)
    """
    
    values = (
        exo_id,
        dof_id,
        rel_props.get('aim'),
        int(rel_props.get('direction', 0)) if rel_props.get('direction') else None,
        rel_props.get('adjustable'),
        rel_props.get('mechanism'),
        rel_props.get('rangeAdjustable'),
        rel_props.get('sizeAdjustable'),
        int(rel_props.get('minAngle', 0)) if rel_props.get('minAngle') else None,
        int(rel_props.get('maxAngle', 0)) if rel_props.get('maxAngle') else None,
        int(rel_props.get('lowerBoundMinAngle', 0)) if rel_props.get('lowerBoundMinAngle') else None,
        int(rel_props.get('lowerBoundMaxAngle', 0)) if rel_props.get('lowerBoundMaxAngle') else None,
        int(rel_props.get('upperBoundMinAngle', 0)) if rel_props.get('upperBoundMinAngle') else None,
        int(rel_props.get('upperBoundMaxAngle', 0)) if rel_props.get('upperBoundMaxAngle') else None
    )
    
    cursor.execute(query, values)

def insert_has_aimtype(cursor, aim_id, aimtype_id):
    """Insert HAS_AIMTYPE relationship"""
    query = """
    INSERT IGNORE INTO HAS_AIMTYPE (aimId, aimTypeId)
    VALUES (%s, %s)
    """
    cursor.execute(query, (aim_id, aimtype_id))

def insert_is_connected_with(cursor, joint_id, part_id):
    """Insert IS_CONNECTED_WITH relationship"""
    query = """
    INSERT IGNORE INTO IS_CONNECTED_WITH (jointTId, partId)
    VALUES (%s, %s)
    """
    cursor.execute(query, (joint_id, part_id))

def insert_limits_in(cursor, exo_id, dof_id, rel_props):
    """Insert LIMITS_IN relationship"""
    query = """
    INSERT INTO LIMITS_IN (exoId, dofId, aim, direction, adjustable, minAngle, maxAngle)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        aim = VALUES(aim),
        direction = VALUES(direction),
        adjustable = VALUES(adjustable),
        minAngle = VALUES(minAngle),
        maxAngle = VALUES(maxAngle)
    """
    
    values = (
        exo_id,
        dof_id,
        rel_props.get('aim'),
        int(rel_props.get('direction', 0)) if rel_props.get('direction') else None,
        rel_props.get('adjustable'),
        int(rel_props.get('minAngle', 0)) if rel_props.get('minAngle') else None,
        int(rel_props.get('maxAngle', 0)) if rel_props.get('maxAngle') else None
    )
    
    cursor.execute(query, values)

def insert_has_skntype(cursor, skn_id, skntype_id):
    """Insert HAS_SKNTYPE relationship"""
    query = """
    INSERT IGNORE INTO HAS_SKNTYPE (structureKinematicNameId, structureKinematicNameTypeId)
    VALUES (%s, %s)
    """
    cursor.execute(query, (skn_id, skntype_id))

def insert_transfers_forces_from(cursor, exo_id, part_id):
    """Insert TRANSFERS_FORCES_FROM relationship"""
    query = """
    INSERT IGNORE INTO TRANSFERS_FORCES_FROM (exoId, partId)
    VALUES (%s, %s)
    """
    cursor.execute(query, (exo_id, part_id))

def insert_transfers_forces_to(cursor, exo_id, part_id):
    """Insert TRANSFERS_FORCES_TO relationship"""
    query = """
    INSERT IGNORE INTO TRANSFERS_FORCES_TO (exoId, partId)
    VALUES (%s, %s)
    """
    cursor.execute(query, (exo_id, part_id))

# ====================
# PROCESSING FUNCTIONS
# ====================

def process_part1(cursor, csv_file_path):
    """Process Part 1: HAS_AIM, HAS_PROPERTY, ASSISTS_IN"""
    print("\n" + "="*60)
    print("PROCESSING PART 1: Main Exo Relationships")
    print("="*60)
    
    stats = {'rows': 0, 'has_aim': 0, 'has_property': 0, 'assists_in': 0}
    
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        
        for row in csv_reader:
            stats['rows'] += 1
            node_n = parse_node(row['n'])
            relationship_r = parse_relationship(row['r'])
            node_m = parse_node(row['m'])
            
            if not node_n:
                continue
            
            exo_id = insert_exo(cursor, node_n, update_mode=True)
            
            if relationship_r and node_m:
                rel_type = relationship_r['type']
                rel_props = relationship_r['properties']
                
                if rel_type == 'HAS_AIM':
                    if node_m['type'] == 'Aim':
                        aim_id = insert_aim(cursor, node_m, update_mode=True)
                        aim_category = rel_props.get('aimCategory', '')
                        insert_has_aim(cursor, exo_id, aim_id, aim_category)
                        stats['has_aim'] += 1
                    elif node_m['type'] == 'StructureKinematicName':
                        structure_id = insert_structure_kinematic_name(cursor, node_m, update_mode=True)
                        category = rel_props.get('structureKinematicNameCategory', '')
                        insert_has_aim_structure(cursor, exo_id, structure_id, category)
                        stats['has_aim'] += 1
                
                elif rel_type == 'HAS_PROPERTY':
                    property_name = node_m['properties'].get('exoPropertyName', '')
                    property_id = get_or_create_property(cursor, property_name)
                    property_value = rel_props.get('exoPropertyValue', '')
                    insert_has_property(cursor, exo_id, property_id, property_value)
                    stats['has_property'] += 1
                
                elif rel_type == 'ASSISTS_IN':
                    if node_m['type'] == 'Dof':
                        dof_id = insert_dof(cursor, node_m, update_mode=True)
                        insert_assists_in(cursor, exo_id, dof_id, rel_props)
                        stats['assists_in'] += 1
    
    print(f"✓ Part 1 Complete - Rows: {stats['rows']}, HAS_AIM: {stats['has_aim']}, "
          f"HAS_PROPERTY: {stats['has_property']}, ASSISTS_IN: {stats['assists_in']}")
    return stats

def process_part2(cursor, csv_file_path):
    """Process Part 2: HAS_DOF, DOESNT_GO_WITH"""
    print("\n" + "="*60)
    print("PROCESSING PART 2: Joint and Constraint Relationships")
    print("="*60)
    
    stats = {'rows': 0, 'has_dof': 0, 'doesnt_go_with': 0}
    
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        
        for row in csv_reader:
            stats['rows'] += 1
            node_n = parse_node(row['n'])
            relationship_r = parse_relationship(row['r'])
            node_m = parse_node(row['m'])
            
            if not node_n or not relationship_r or not node_m:
                continue
            
            rel_type = relationship_r['type']
            
            if rel_type == 'HAS_DOF':
                if node_n['type'] == 'JointT' and node_m['type'] == 'Dof':
                    joint_id = insert_joint_t(cursor, node_n, update_mode=True)
                    dof_id = insert_dof(cursor, node_m, update_mode=True)
                    insert_has_dof(cursor, joint_id, dof_id)
                    stats['has_dof'] += 1
            
            elif rel_type == 'DOESNT_GO_WITH':
                if node_n['type'] == 'Exo' and node_m['type'] == 'StructureKinematicName':
                    exo_id = insert_exo(cursor, node_n, update_mode=False)
                    structure_id = insert_structure_kinematic_name(cursor, node_m, update_mode=False)
                    insert_doesnt_go_with(cursor, exo_id, structure_id)
                    stats['doesnt_go_with'] += 1
    
    print(f"✓ Part 2 Complete - Rows: {stats['rows']}, HAS_DOF: {stats['has_dof']}, "
          f"DOESNT_GO_WITH: {stats['doesnt_go_with']}")
    return stats

def process_part3(cursor, csv_file_path):
    """Process Part 3: HAS_AS_MAIN_DOF, GIVES_RESISTANCE_IN, HAS_AIMTYPE"""
    print("\n" + "="*60)
    print("PROCESSING PART 3: DOF and AimType Relationships")
    print("="*60)
    
    stats = {'rows': 0, 'has_main_dof': 0, 'gives_resistance': 0, 'has_aimtype': 0}
    
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        
        for row in csv_reader:
            stats['rows'] += 1
            node_n = parse_node(row['n'])
            relationship_r = parse_relationship(row['r'])
            node_m = parse_node(row['m'])
            
            if not node_n or not relationship_r or not node_m:
                continue
            
            rel_type = relationship_r['type']
            rel_props = relationship_r['properties']
            
            if rel_type == 'HAS_AS_MAIN_DOF':
                if node_n['type'] == 'Exo' and node_m['type'] == 'Dof':
                    exo_id = insert_exo(cursor, node_n, update_mode=False)
                    dof_id = insert_dof(cursor, node_m, update_mode=False)
                    insert_has_as_main_dof(cursor, exo_id, dof_id)
                    stats['has_main_dof'] += 1
            
            elif rel_type == 'GIVES_RESISTANCE_IN':
                if node_n['type'] == 'Exo' and node_m['type'] == 'Dof':
                    exo_id = insert_exo(cursor, node_n, update_mode=False)
                    dof_id = insert_dof(cursor, node_m, update_mode=False)
                    insert_gives_resistance_in(cursor, exo_id, dof_id, rel_props)
                    stats['gives_resistance'] += 1
            
            elif rel_type == 'HAS_AIMTYPE':
                if node_n['type'] == 'Aim' and node_m['type'] == 'AimType':
                    aim_id = insert_aim(cursor, node_n, update_mode=False)
                    aimtype_id = get_or_create_aimtype(cursor, node_m)
                    insert_has_aimtype(cursor, aim_id, aimtype_id)
                    stats['has_aimtype'] += 1
    
    print(f"✓ Part 3 Complete - Rows: {stats['rows']}, HAS_AS_MAIN_DOF: {stats['has_main_dof']}, "
          f"GIVES_RESISTANCE_IN: {stats['gives_resistance']}, HAS_AIMTYPE: {stats['has_aimtype']}")
    return stats

def process_part4(cursor, csv_file_path):
    """Process Part 4: IS_CONNECTED_WITH, LIMITS_IN, HAS_SKNTYPE"""
    print("\n" + "="*60)
    print("PROCESSING PART 4: Part Connections and Limits")
    print("="*60)
    
    stats = {'rows': 0, 'is_connected': 0, 'limits_in': 0, 'has_skntype': 0}
    
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        
        for row in csv_reader:
            stats['rows'] += 1
            node_n = parse_node(row['n'])
            relationship_r = parse_relationship(row['r'])
            node_m = parse_node(row['m'])
            
            if not node_n or not relationship_r or not node_m:
                continue
            
            rel_type = relationship_r['type']
            rel_props = relationship_r['properties']
            
            if rel_type == 'IS_CONNECTED_WITH':
                if node_n['type'] == 'JointT' and node_m['type'] == 'Part':
                    joint_id = insert_joint_t(cursor, node_n, update_mode=False)
                    part_id = insert_part(cursor, node_m, update_mode=True)
                    insert_is_connected_with(cursor, joint_id, part_id)
                    stats['is_connected'] += 1
            
            elif rel_type == 'LIMITS_IN':
                if node_n['type'] == 'Exo' and node_m['type'] == 'Dof':
                    exo_id = insert_exo(cursor, node_n, update_mode=False)
                    dof_id = insert_dof(cursor, node_m, update_mode=False)
                    insert_limits_in(cursor, exo_id, dof_id, rel_props)
                    stats['limits_in'] += 1
            
            elif rel_type == 'HAS_SKNTYPE':
                if node_n['type'] == 'StructureKinematicName' and node_m['type'] == 'StructureKinematicNameType':
                    skn_id = insert_structure_kinematic_name(cursor, node_n, update_mode=False)
                    skntype_id = get_or_create_structure_kinematic_name_type(cursor, node_m)
                    insert_has_skntype(cursor, skn_id, skntype_id)
                    stats['has_skntype'] += 1
    
    print(f"✓ Part 4 Complete - Rows: {stats['rows']}, IS_CONNECTED_WITH: {stats['is_connected']}, "
          f"LIMITS_IN: {stats['limits_in']}, HAS_SKNTYPE: {stats['has_skntype']}")
    return stats

def process_part5(cursor, csv_file_path):
    """Process Part 5: TRANSFERS_FORCES_FROM, TRANSFERS_FORCES_TO"""
    print("\n" + "="*60)
    print("PROCESSING PART 5: Force Transfer Relationships")
    print("="*60)
    
    stats = {'rows': 0, 'transfers_from': 0, 'transfers_to': 0}
    
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        
        for row in csv_reader:
            stats['rows'] += 1
            node_n = parse_node(row['n'])
            relationship_r = parse_relationship(row['r'])
            node_m = parse_node(row['m'])
            
            if not node_n or not relationship_r or not node_m:
                continue
            
            rel_type = relationship_r['type']
            
            if rel_type == 'TRANSFERS_FORCES_FROM':
                if node_n['type'] == 'Exo' and node_m['type'] == 'Part':
                    exo_id = insert_exo(cursor, node_n, update_mode=False)
                    part_id = insert_part(cursor, node_m, update_mode=False)
                    insert_transfers_forces_from(cursor, exo_id, part_id)
                    stats['transfers_from'] += 1
            
            elif rel_type == 'TRANSFERS_FORCES_TO':
                if node_n['type'] == 'Exo' and node_m['type'] == 'Part':
                    exo_id = insert_exo(cursor, node_n, update_mode=False)
                    part_id = insert_part(cursor, node_m, update_mode=False)
                    insert_transfers_forces_to(cursor, exo_id, part_id)
                    stats['transfers_to'] += 1
    
    print(f"✓ Part 5 Complete - Rows: {stats['rows']}, TRANSFERS_FORCES_FROM: {stats['transfers_from']}, "
          f"TRANSFERS_FORCES_TO: {stats['transfers_to']}")
    return stats

def process_part6(cursor, csv_file_path):
    """Process Part 6: GIVES_POSTURAL_SUPPORT_IN"""
    print("\n" + "="*60)
    print("PROCESSING PART 6: Postural Support Relationships")
    print("="*60)
    
    stats = {'rows': 0, 'gives_postural_support': 0}
    
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        
        for row in csv_reader:
            stats['rows'] += 1
            node_n = parse_node(row['n'])
            relationship_r = parse_relationship(row['r'])
            node_m = parse_node(row['m'])
            
            if not node_n or not relationship_r or not node_m:
                continue
            
            rel_type = relationship_r['type']
            rel_props = relationship_r['properties']
            
            if rel_type == 'GIVES_POSTURAL_SUPPORT_IN':
                if node_n['type'] == 'Exo' and node_m['type'] == 'Dof':
                    exo_id = insert_exo(cursor, node_n, update_mode=False)
                    dof_id = insert_dof(cursor, node_m, update_mode=False)
                    insert_gives_postural_support_in(cursor, exo_id, dof_id, rel_props)
                    stats['gives_postural_support'] += 1
    
    print(f"✓ Part 6 Complete - Rows: {stats['rows']}, "
          f"GIVES_POSTURAL_SUPPORT_IN: {stats['gives_postural_support']}")
    return stats

# ====================
# MAIN EXECUTION
# ====================

def main():
    """Main execution function"""
    print("\n" + "="*60)
    print("EXOSKELETON DATABASE IMPORTER")
    print("="*60)
    print("This script will import all CSV files into the MySQL database.")
    print("="*60)
    
    # Connect to database
    connection = connect_db()
    if not connection:
        print("Failed to connect to database. Exiting.")
        return
    
    cursor = connection.cursor()
    all_stats = {}
    
    try:
        # Process Part 1
        try:
            all_stats['part1'] = process_part1(cursor, CSV_FILES['part1'])
            connection.commit()
        except FileNotFoundError:
            print(f"⚠ Warning: {CSV_FILES['part1']} not found. Skipping Part 1.")
        except Exception as e:
            print(f"✗ Error in Part 1: {e}")
            connection.rollback()
        
        # Process Part 2
        try:
            all_stats['part2'] = process_part2(cursor, CSV_FILES['part2'])
            connection.commit()
        except FileNotFoundError:
            print(f"⚠ Warning: {CSV_FILES['part2']} not found. Skipping Part 2.")
        except Exception as e:
            print(f"✗ Error in Part 2: {e}")
            connection.rollback()
        
        # Process Part 3
        try:
            all_stats['part3'] = process_part3(cursor, CSV_FILES['part3'])
            connection.commit()
        except FileNotFoundError:
            print(f"⚠ Warning: {CSV_FILES['part3']} not found. Skipping Part 3.")
        except Exception as e:
            print(f"✗ Error in Part 3: {e}")
            connection.rollback()
        
        # Process Part 4
        try:
            all_stats['part4'] = process_part4(cursor, CSV_FILES['part4'])
            connection.commit()
        except FileNotFoundError:
            print(f"⚠ Warning: {CSV_FILES['part4']} not found. Skipping Part 4.")
        except Exception as e:
            print(f"✗ Error in Part 4: {e}")
            connection.rollback()
        
        # Process Part 5
        try:
            all_stats['part5'] = process_part5(cursor, CSV_FILES['part5'])
            connection.commit()
        except FileNotFoundError:
            print(f"⚠ Warning: {CSV_FILES['part5']} not found. Skipping Part 5.")
        except Exception as e:
            print(f"✗ Error in Part 5: {e}")
            connection.rollback()
        
        # Process Part 6
        try:
            all_stats['part6'] = process_part6(cursor, CSV_FILES['part6'])
            connection.commit()
        except FileNotFoundError:
            print(f"⚠ Warning: {CSV_FILES['part6']} not found. Skipping Part 6.")
        except Exception as e:
            print(f"✗ Error in Part 6: {e}")
            connection.rollback()
        
        # Final summary
        print("\n" + "="*60)
        print("FINAL IMPORT SUMMARY")
        print("="*60)
        
        total_rows = sum(stats.get('rows', 0) for stats in all_stats.values())
        print(f"Total rows processed across all files: {total_rows}")
        
        for part_name, stats in all_stats.items():
            print(f"\n{part_name.upper()}:")
            for key, value in stats.items():
                print(f"  {key}: {value}")
        
        print("\n" + "="*60)
        print("✓ ALL IMPORTS COMPLETED SUCCESSFULLY!")
        print("="*60)
        
    except Error as e:
        print(f"\n✗ Database error: {e}")
        connection.rollback()
    
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        connection.rollback()
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("\nMySQL connection closed")

if __name__ == "__main__":
    main()