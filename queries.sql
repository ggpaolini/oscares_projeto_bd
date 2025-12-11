1- Quantas nomeações existem na base de dados no total?

select count(*) from nomination

2-Listar todas as categorias da classe "Directing".

select * from category where classname="Directing"

3-Mostrar nomeados que são empresas

select select * from nominee where nomineeid like "co%"

4-Listar os filmes que venceram o prémio de "Best Picture" (Melhor Filme).

select filmid, filmname from film
natural join nomination_name
natural join nomination
where categoryname="Best Picture" and winner="TRUE"

5-Número médio de nomeados por cerimónia

SELECT AVG(NumNominees) AS AvgNominees
FROM (
    SELECT CeremonyNumber, COUNT(*) AS NumNominees
    FROM NOMINATION
    GROUP BY CeremonyNumber
)

6-Top 5 de Atores/Atrizes com mais vitórias na história.

select nomineeid, name, count(winner) as wins from nominee
natural join nomination_nominee
natural join nomination
where winner="TRUE" and nomineeid not like "co%"
group by nomineeid
order by count(winner) desc
limit 5

7- Filmes com mais nomeações numa única cerimónia.

select filmid, filmname, count(*) as N_Nomeações from film
natural join nomination_film
natural join nomination
group by filmid, filmname, ceremonynumber 
order by N_Nomeações desc

8-Listar todos os indivíduos nomeados por "The Godfather".

select distinct nomineeid, name
from nominee
natural join nomination_nominee
natural join nomination
natural join nomination_film
where filmname="The Godfather"
and nomineeid not like "co%"


9- Todos os filmes que ganharam todas as categorias em que foram nomeados.

SELECT FilmId, FilmName
FROM FILM
WHERE FilmId NOT IN (

    -- filmes que têm alguma nomeação não vencedora
    SELECT NF.FilmId
    FROM NOMINATION_FILM NF
    NATURAL JOIN NOMINATION N
    WHERE NF.FilmId NOT IN (
        -- nomeações desse filme que foram vencedoras
        SELECT NF2.FilmId
        FROM NOMINATION_FILM NF2
        NATURAL JOIN NOMINATION N2
        WHERE N2.Winner = 'TRUE'
          AND NF2.FilmId = NF.FilmId
    )
)
10-Atores que venceram Oscars em anos consecutivos.

WITH wins AS (
    SELECT NomineeId, Name, CeremonyNumber
    FROM NOMINATION
    NATURAL JOIN NOMINATION_NOMINEE
    NATURAL JOIN NOMINEE
    WHERE Winner = 'TRUE'
)
SELECT w1.NomineeId, w1.Name, w1.CeremonyNumber AS Year1, w2.CeremonyNumber AS Year2
FROM wins w1
JOIN wins w2
    ON w1.NomineeId = w2.NomineeId
   AND w2.CeremonyNumber = w1.CeremonyNumber + 1
ORDER BY w1.NomineeId, w1.CeremonyNumber;