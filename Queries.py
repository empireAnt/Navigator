import psycopg2
import re
import test

TRUNCATE_CE_PRODUCT = ['''
truncate table openidconnectclient$clientconfiguration;
truncate table emailtemplate$emailsettings;
Update emailtemplate$recipient SET otheremailaddress = 'Test@chubb.com';
update products$product
set bypasssanctions = true;
update general$serviceconfiguration
set password =
case
when userprofile = 'ProductGroupApp' then '{AES}d7zflKOqK4bDIv0gDtBS9w==;76CuoNZc57EHwZTzS7OcRg=='
when userprofile = 'DnBLookUp' then '{AES}/hjRGTnXNx9zW6gIA0ty3g==;aM+0npBskW9FQKJBUNCi2w=='
when userprofile = 'Informa_DnB' then '{AES}nzWR0iY4LP2fsP3WD4Lrvw==;UrnrRIqUqqtSuxmMV3cufg=='
when userprofile = 'CyberSignalSubscriptionKey' then '{AES}TQGKuPHuuf0qhtTnGymyJg==;VTPa5e39y1x9u5ZZrHHTfy/IxXrynX+5Kr9NRftJrSP2pxIceFtc4z42svqZ0Kq/'
else password
end;
update parties$brokeremployee
set phone = case when phone is not null and phone != '' then '0000000000' else phone end,
mobile = case when mobile is not null and mobile != '' then '0000000000' else mobile end;
update parties$chubbuser
set phone = case when phone is not null and phone != '' then '0000000000' else phone end;
update system$user
set password = '{BCrypt}$2a$10$WARotPMW/ncGFh5C9iWsPOnubml2IrLDvQLL4SK1zKpcaCQJvAj2a'
where name in
(
	'Martina.Vella@Chubb.com', 'EleanaMayra.Fernandez@Chubb.com', 'Emanuele.Provenzale@Chubb.com', 'karine.ragai@chubb.com'
);
UPDATE documentgeneration$quadientconfiguration SET 
quadientservice = 'https://uat.emea.studiogateway.chubb.com/enterprise.system.chubbio-document-gen-connector/generate',
destinationurl = 'https://scaler.emea-test.chubb.quadient.cloud/rest/api/submit-job/DocumentGenerationAPI1',
userid = 'IgniteUAT';
UPDATE apimauthentication$apimconfigencrypted SET
apimclientsecret = '{AES3}OhX8Q35KahNmi+Yf;oqQKOAMKXzEfhjfVX4OrtxkcK8eIGBW4yPb29yRXzLsI+xSCUnYDf8TZ6L2ZyipD1RoM3kdTmjQ=',
apimresource = 'ada821e9-fcbd-45c9-8edf-cf80e1a75876',
apimclientid = '{AES3}JzP50GXaroN+sUTh;gmOYqAKevbM8B9cbkliQtz/+ix+snrwvDU3DI7CfisJZNBLu6cID+8+lLOCpKMbm/zTK5A=='
WHERE apimconfigfor = 'Quadient';
'''
]
TRUNCATE_CE_REGION = ['''
update system$user
set password = '{BCrypt}$2a$10$WARotPMW/ncGFh5C9iWsPOnubml2IrLDvQLL4SK1zKpcaCQJvAj2a'
where name in
(
	'Martina.Vella@Chubb.com', 'EleanaMayra.Fernandez@Chubb.com', 'Emanuele.Provenzale@Chubb.com', 'karine.ragai@chubb.com'
);
Update emailtemplate$recipient SET otheremailaddress = 'Test@chubb.com';
truncate table openidconnectprovider$registeredclient;
truncate table openidconnectprovider$jsonwebkey;
truncate table general$productgroupapp;
truncate table emailtemplate$emailsettings;
update general$xpressionsettings
set xpressionusername = 'svc_euuaxp_ign', xpressionpassword = '{AES3}i9bbaryY8UbyHtIi;Eqs5wpyujF454CfFzVxpTsDpoL9Z+Bi4qAhEdZeP/3Ap0sSwLnCcbw==';
update general$serviceconfiguration
set password =
case
when userprofile = 'ProductGroupApp' then '{AES}d7zflKOqK4bDIv0gDtBS9w==;76CuoNZc57EHwZTzS7OcRg=='
when userprofile = 'DnBLookUp' then '{AES}/hjRGTnXNx9zW6gIA0ty3g==;aM+0npBskW9FQKJBUNCi2w=='
when userprofile = 'Informa_DnB' then '{AES}nzWR0iY4LP2fsP3WD4Lrvw==;UrnrRIqUqqtSuxmMV3cufg=='
else password
end;
update parties$brokeremployee
set phone = case when phone is not null and phone != '' then '0000000000' else phone end,
mobile = case when mobile is not null and mobile != '' then '0000000000' else mobile end;
update parties$chubbuser
set phone = case when phone is not null and phone != '' then '0000000000' else phone
end;
                      ''']
TRUNCATE_CADENCE = ['''
truncate table openidconnectclient$clientconfiguration;
truncate table emailtemplate$emailsettings;
Update emailtemplate$recipient
SET otheremailaddress = 'Test@chubb.com';
update products$product
set productgroupappurl = 'http://ff.ignite.local:9980';
update parties$brokeremployee set phone = case when phone is not null then '0000000000' else phone end, mobile = case when mobile is not null then '0000000000' else mobile end;
update parties$chubbuser set phone = case when phone is not null then '0000000000' else phone end;
update system$user
set password = '{BCrypt}$2a$10$WARotPMW/ncGFh5C9iWsPOnubml2IrLDvQLL4SK1zKpcaCQJvAj2a'
where name in
(
	'Martina.Vella@Chubb.com', 'EleanaMayra.Fernandez@Chubb.com', 'Emanuele.Provenzale@Chubb.com', 'karine.ragai@chubb.com'
);
'''
]
LOGIN_USERS = ['''
WITH usernames AS (
  SELECT u.name
  FROM "system$user" u
  INNER JOIN "system$userroles" ur ON ur."system$userid" = u.id
  INNER JOIN "system$userrole" urole ON urole.id = ur."system$userroleid"
  INNER JOIN "useradministration$account" a ON a.id = u.id
  LEFT JOIN "parties$underwriter_account" ua ON ua."useradministration$accountid" = a.id
  LEFT JOIN "parties$chubbuser" uw ON uw.id = ua."parties$chubbuserid"
  LEFT JOIN "products$underwriterproductaccess_underwriter" upau ON upau."parties$chubbuserid" = uw.id
  LEFT JOIN "products$transactionaluserproductaccess" tupa ON tupa.id = upau."products$transactionaluserproductaccessid"
  LEFT JOIN "products$transactionaluserproductaccess_product" tupap ON tupap."products$transactionaluserproductaccessid" = tupa.id
  LEFT JOIN "products$product" pro ON pro.id = tupap."products$productid"
  WHERE tupa."accesstype" = 'Underwriter'
  GROUP BY uw.id, u.id, pro.id, tupa.id
  HAVING LENGTH(string_agg(urole.name, ' | ' ORDER BY urole.id)) > 50
  ORDER BY pro.productname
  LIMIT 5
)
UPDATE system$user u
SET password = '{BCrypt}$2a$10$WARotPMW/ncGFh5C9iWsPOnubml2IrLDvQLL4SK1zKpcaCQJvAj2a'
FROM usernames
WHERE u.name = usernames.name
RETURNING u.name
    ''']
VALIDATION_QUERIES = ["SELECT * FROM openidconnectclient$clientconfiguration", "SELECT * FROM emailtemplate$emailsettings", "SELECT * FROM emailtemplate$recipient"]
RISK_QUERY = '''
select R.uniqueid
from risks$risk R
left join risks$quote_risk Q_R on Q_R.risks$riskid = R.id
left join risks$quote Q on Q_R.risks$quoteid = Q.id
left join risks$policy_risk P_R on R.id = P_R.risks$riskid
left join risks$policy P on P_R.risks$policyid = P.id
where r.iscurrent
and (policynumber ilike '%%' OR quotenumber = '')
order by R.uniqueid desc             
              '''
CURRENT_DATABASE = ''

def execute_queries(queries, db_name = CURRENT_DATABASE, psw = '1234'):

    connection = psycopg2.connect(
        host='localhost',
        dbname=db_name,
        user='postgres',
        password=psw,
        port=5432
    )
    cursor = connection.cursor()
    results = []
    if isinstance(queries, str):
        queries = [queries]
    for query in queries:
        cursor.execute(query)
        try:
            result = cursor.fetchall()
        except Exception:
            result = None
        results.append(result)
        connection.commit()
    cursor.close()
    connection.close()
    return results

def execute_single_query(query, db_name = CURRENT_DATABASE, psw = '1234'):

    connection = psycopg2.connect(
        host='localhost',
        dbname=db_name,
        user='postgres',
        password=psw,
        port=5432
    )
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchone()
    return result

def getDBQueries(db_name):
    if 'REGION' in db_name.upper():
        return TRUNCATE_CE_REGION
    elif 'CADENCE' in db_name.upper():
        return TRUNCATE_CADENCE
    else:
        return TRUNCATE_CE_PRODUCT

def get_uniqueid(input_number):
    query = f'''select R.uniqueid
    from risks$risk R
    left join risks$quote_risk Q_R on Q_R.risks$riskid = R.id
    left join risks$quote Q on Q_R.risks$quoteid = Q.id
    left join risks$policy_risk P_R on R.id = P_R.risks$riskid
    left join risks$policy P on P_R.risks$policyid = P.id
    where r.iscurrent
    and (policynumber = '{input_number}' OR quotenumber = '{input_number}')
    order by R.uniqueid desc
    '''
    return execute_single_query(query)[0]

def set_DB(db_name):
    global CURRENT_DATABASE
    CURRENT_DATABASE = db_name

def get_quadient_inputs(product_name, ):
    select_query = f'''
    SELECT productfamily, producttype, countrycode FROM products$product p
    JOIN products$country_product cp ON p.id = cp.products$productid
    JOIN parties$country c ON c.id = cp.parties$countryid
    WHERE productname = {product_name}
    '''