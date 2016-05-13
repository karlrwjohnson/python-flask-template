create table foo (a int primary key, b int);
create table bar (a int not null references foo(a), b int);

# This schema table relates foreign keys in child tables to primary keys in parent tables
select * from information_schema.referential_constraints;
 constraint_catalog | constraint_schema | constraint_name | unique_constraint_catalog | unique_constraint_schema | unique_constraint_name | match_option | update_rule | delete_rule 
--------------------+-------------------+-----------------+---------------------------+--------------------------+------------------------+--------------+-------------+-------------
 kjohnson           | public            | bar_a_fkey      | kjohnson                  | public                   | foo_pkey               | NONE         | NO ACTION   | NO ACTION
(1 row)

# This schema table lists the columns which appear in a child table
select * from information_schema.key_column_usage;
 constraint_catalog | constraint_schema | constraint_name | table_catalog | table_schema | table_name | column_name | ordinal_position | position_in_unique_constraint 
--------------------+-------------------+-----------------+---------------+--------------+------------+-------------+------------------+-------------------------------
 kjohnson           | public            | foo_pkey        | kjohnson      | public       | foo        | a           |                1 |                            ␀ 
 kjohnson           | public            | bar_a_fkey      | kjohnson      | public       | bar        | a           |                1 |                             1
(2 rows)

# This metadata table is useless.
select * from information_schema.constraint_column_usage ;
 table_catalog | table_schema | table_name | column_name | constraint_catalog | constraint_schema | constraint_name 
---------------+--------------+------------+-------------+--------------------+-------------------+-----------------
 kjohnson      | public       | foo        | a           | kjohnson           | public            | bar_a_fkey
 kjohnson      | public       | foo        | a           | kjohnson           | public            | foo_pkey
(2 rows)

#############################################################################

# This query prints out the foreign key relationships in a database, so long as the foreign keys are on single fields
# On a composite foreign key, it would probably return N*M rows.
select pkey_column.table_name parent_table,
       pkey_column.column_name parent_column,
       pkey_column.constraint_name pkey_constraint,
       fkey_column.table_name child_table,
       fkey_column.column_name child_column,
       fkey_column.constraint_name fkey_constraint,
       ref_cons.update_rule,
       ref_cons.delete_rule
from information_schema.referential_constraints ref_cons
inner join information_schema.key_column_usage fkey_column
        on ref_cons.constraint_name = fkey_column.constraint_name
inner join information_schema.key_column_usage pkey_column
        on ref_cons.unique_constraint_name = pkey_column.constraint_name
;

###########################################
# Now, let's try composite foreign keys

create table foo (
    a int not null, 
    b int not null,
    primary key(a, b)
);

create table bar (
    f_b int not null, -- Let's switch the order to see how it's handled
    f_a int not null,
    data text,
    foreign key (f_b, f_a) references foo(b, a) match full on delete cascade
);

# And let's run the above query...
 parent_table | parent_column | pkey_constraint | child_table | child_column | fkey_constraint | update_rule | delete_rule 
--------------+---------------+-----------------+-------------+--------------+-----------------+-------------+-------------
 foo          | a             | foo_pkey        | bar         | f_b          | bar_f_b_fkey    | NO ACTION   | CASCADE
 foo          | a             | foo_pkey        | bar         | f_a          | bar_f_b_fkey    | NO ACTION   | CASCADE
 foo          | b             | foo_pkey        | bar         | f_b          | bar_f_b_fkey    | NO ACTION   | CASCADE
 foo          | b             | foo_pkey        | bar         | f_a          | bar_f_b_fkey    | NO ACTION   | CASCADE
(4 rows)

# Called it. Need to fix the query.
select * from information_schema.referential_constraints;
 constraint_catalog | constraint_schema | constraint_name | unique_constraint_catalog | unique_constraint_schema | unique_constraint_name | match_option | update_rule | delete_rule 
--------------------+-------------------+-----------------+---------------------------+--------------------------+------------------------+--------------+-------------+-------------
 kjohnson           | public            | bar_f_b_fkey    | kjohnson                  | public                   | foo_pkey               | FULL         | NO ACTION   | CASCADE
(1 row)

select * from information_schema.key_column_usage;
 constraint_catalog | constraint_schema | constraint_name | table_catalog | table_schema | table_name | column_name | ordinal_position | position_in_unique_constraint 
--------------------+-------------------+-----------------+---------------+--------------+------------+-------------+------------------+-------------------------------
 kjohnson           | public            | foo_pkey        | kjohnson      | public       | foo        | a           |                1 |                            ␀ 
 kjohnson           | public            | foo_pkey        | kjohnson      | public       | foo        | b           |                2 |                            ␀ 
 kjohnson           | public            | bar_f_b_fkey    | kjohnson      | public       | bar        | f_b         |                1 |                             2
 kjohnson           | public            | bar_f_b_fkey    | kjohnson      | public       | bar        | f_a         |                2 |                             1
(4 rows)

# OK, so a couple things:
# - Switching the order was a good idea. We can see the fkeys take care of re-mapping the order.
# - The pkey has no position_in_unique_constraint. Probably because pkeys don't reference anything
#   --> It already IS a "unique constraint"
#   ... Maybe I should be calling it a "ukey" (unique key) in the query instead of a "pkey"
# - I need to figure out how to build arrays. Grrr...

select parent_key_col.table_name parent_table,
       parent_key_col.column_name parent_column,
       parent_key_col.constraint_name pkey_constraint,
       child_key_col.table_name child_table,
       child_key_col.column_name child_column,
       child_key_col.constraint_name fkey_constraint,
       ref_cons.update_rule,
       ref_cons.delete_rule
from information_schema.referential_constraints ref_cons
inner join information_schema.key_column_usage parent_key_col
        on ref_cons.unique_constraint_name = parent_key_col.constraint_name
inner join information_schema.key_column_usage child_key_col
        on ref_cons.constraint_name = child_key_col.constraint_name
       and parent_key_col.ordinal_position = child_key_col.position_in_unique_constraint
;

 parent_table | parent_column | pkey_constraint | child_table | child_column | fkey_constraint | update_rule | delete_rule 
--------------+---------------+-----------------+-------------+--------------+-----------------+-------------+-------------
 foo          | a             | foo_pkey        | bar         | f_a          | bar_f_b_fkey    | NO ACTION   | CASCADE
 foo          | b             | foo_pkey        | bar         | f_b          | bar_f_b_fkey    | NO ACTION   | CASCADE
(2 rows)

# Looks right, and no arrays required! :)
# I probably want to group by fkey_constraint though, and pkey_constraint is basically useless
# Also, when I go to add the "where" clauses to filter by table, I'll want to rearrange the joins to weed out tables faster.
# Maybe make it a subquery?
# ... Nah, no subqueries. Optimization is dangerous: It takes time, it's hard to do right, and unless you know what
# you're doing, you'll likely do it wrong.

# I discovered another place to get the table names. This would let me group the columns into their own array with a query
# and derive the table name separately.
select * from information_schema.table_constraints where table_schema = 'public';
 constraint_catalog | constraint_schema |    constraint_name    | table_catalog | table_schema | table_name | constraint_type | is_deferrable | initially_deferred 
--------------------+-------------------+-----------------------+---------------+--------------+------------+-----------------+---------------+--------------------
 kjohnson           | public            | foo_pkey              | kjohnson      | public       | foo        | PRIMARY KEY     | NO            | NO
 kjohnson           | public            | bar_f_b_fkey          | kjohnson      | public       | bar        | FOREIGN KEY     | NO            | NO
 kjohnson           | public            | 2200_59454_1_not_null | kjohnson      | public       | foo        | CHECK           | NO            | NO
 kjohnson           | public            | 2200_59454_2_not_null | kjohnson      | public       | foo        | CHECK           | NO            | NO
 kjohnson           | public            | 2200_59481_1_not_null | kjohnson      | public       | bar        | CHECK           | NO            | NO
 kjohnson           | public            | 2200_59481_2_not_null | kjohnson      | public       | bar        | CHECK           | NO            | NO
(6 rows)

select ref_cons.constraint_name fkey_constraint,
       ref_cons.update_rule update_rule,
       ref_cons.delete_rule delete_rule,
       (select tab_cons.table_name
        from information_schema.table_constraints tab_cons
        where tab_cons.constraint_name = ref_cons.unique_constraint_name
       ) parent_table,
       (select tab_cons.table_name
        from information_schema.table_constraints tab_cons
        where tab_cons.constraint_name = ref_cons.constraint_name
       ) child_table,
       array(select json_build_object(
                      'parent', parent_key_col.column_name,
                      'child',  child_key_col.column_name
                    )
             from (select column_name,
                          ordinal_position
                   from information_schema.key_column_usage
                   where constraint_name = ref_cons.unique_constraint_name
                  ) parent_key_col
             inner join (select column_name,
                                position_in_unique_constraint
                         from information_schema.key_column_usage
                         where constraint_name = ref_cons.constraint_name
                        ) child_key_col
             on parent_key_col.ordinal_position = child_key_col.position_in_unique_constraint
       ) columns
from information_schema.referential_constraints ref_cons
order by parent_table
;
# ^^ This is disgusting. I definitely overdid it on the subqueries. Also, I'm not totally sure
# how I'm going to filter by table early

# This one has two fewer subqueries. "EXPLAIN ANALYZE" can't tell the difference between them in run-time
select ref_cons.constraint_name fkey_constraint,
       ref_cons.update_rule update_rule,
       ref_cons.delete_rule delete_rule,
       (select tab_cons.table_name
        from information_schema.table_constraints tab_cons
        where tab_cons.constraint_name = ref_cons.unique_constraint_name
       ) parent_table,
       (select tab_cons.table_name
        from information_schema.table_constraints tab_cons
        where tab_cons.constraint_name = ref_cons.constraint_name
       ) child_table,
       array(select json_build_object(
                      'parent', parent_key_col.column_name,
                      'child',  child_key_col.column_name
                    )
             from information_schema.key_column_usage parent_key_col
             inner join information_schema.key_column_usage child_key_col
                     on parent_key_col.ordinal_position = child_key_col.position_in_unique_constraint
             where parent_key_col.constraint_name = ref_cons.unique_constraint_name
               and child_key_col.constraint_name = ref_cons.constraint_name
       ) columns
from information_schema.referential_constraints ref_cons
order by parent_table
;

# Eliminated most of the subqueries. Still kinda weird.
#  - I'm not sure about using json_build_object just to pass around named tuples, although I'm planning to JSON-serialize this anyway
#  - The re-definition of ref_cons in the middle is a code smell just to make the tables inner join.
#    Maybe Postgres already knows how to move around where clauses; I could check with EXPLAIN, but I don't know how to read it.
#    Heck, I'll just do it!
select ref_cons.constraint_name fkey_constraint,
       ref_cons.update_rule update_rule,
       ref_cons.delete_rule delete_rule,
       parent_tab_cons.table_name parent_table,
       child_tab_cons.table_name child_table,
       array(select json_build_object(
                      'parent', parent_key_col.column_name,
                      'child',  child_key_col.column_name
                    )
             from (select ref_cons.constraint_name constraint_name, ref_cons.unique_constraint_name unique_constraint_name) ref_cons
             inner join information_schema.key_column_usage parent_key_col
                     on parent_key_col.constraint_name = ref_cons.unique_constraint_name
             inner join information_schema.key_column_usage child_key_col
                     on child_key_col.constraint_name = ref_cons.constraint_name
                    and parent_key_col.ordinal_position = child_key_col.position_in_unique_constraint
       ) columns
from information_schema.referential_constraints ref_cons
inner join information_schema.table_constraints parent_tab_cons
        on parent_tab_cons.constraint_name = ref_cons.unique_constraint_name
inner join information_schema.table_constraints child_tab_cons
        on child_tab_cons.constraint_name = ref_cons.constraint_name
order by parent_table
;

    select ref_cons.constraint_name   fkey_constraint,
           ref_cons.update_rule       update_rule,
           ref_cons.delete_rule       delete_rule,
           parent_tab_cons.table_name parent_table,
           child_tab_cons.table_name  child_table,
           array(    select json_build_object(
                              'parent', parent_key_col.column_name,
                              'child',  child_key_col.column_name
                            )
                       from information_schema.key_column_usage parent_key_col
                 inner join information_schema.key_column_usage child_key_col
                         on parent_key_col.ordinal_position = child_key_col.position_in_unique_constraint
                      where parent_key_col.constraint_name  = ref_cons.unique_constraint_name
                        and child_key_col.constraint_name   = ref_cons.constraint_name
           ) columns
      from information_schema.referential_constraints ref_cons
inner join information_schema.table_constraints       parent_tab_cons
        on parent_tab_cons.constraint_name = ref_cons.unique_constraint_name
inner join information_schema.table_constraints       child_tab_cons
        on child_tab_cons.constraint_name = ref_cons.constraint_name
;
