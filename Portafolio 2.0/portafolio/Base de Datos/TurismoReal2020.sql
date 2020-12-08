create user turismoreal2020 identified by oracle;

grant connect, resource to turismoreal2020;

alter user turismoreal2020 default tablespace users quota unlimited on users; 

