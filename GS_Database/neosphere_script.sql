-- scripts de limpeza do banco antes de criar
drop table previsao_dado cascade constraints;
drop table acao_preventiva cascade constraints;
drop table usuario cascade constraints;
drop table evento_impacto cascade constraints;
drop table impacto cascade constraints;
drop table alerta cascade constraints;
drop table orgao_responsavel cascade constraints;
drop table previsao cascade constraints;
drop table dado_meteorologico cascade constraints;
drop table sensor cascade constraints;
drop table evento_climatico cascade constraints;
drop table regiao cascade constraints;

drop sequence seq_regiao;
drop sequence seq_evento;
drop sequence seq_sensor;
drop sequence seq_dado;
drop sequence seq_previsao;
drop sequence seq_orgao;
drop sequence seq_alerta;
drop sequence seq_impacto;
drop sequence seq_usuario;
drop sequence seq_acao;

-- Criando as tabelas e suas sequencias

create table REGIAO (
    id_regiao number(10) not null,
    nome varchar2(120) not null,
    estado char(2) not null,
    tipo_relevo varchar2(40),
    latitude number(9,6),
    longitude number(9,6),
    nivel_vulnerabilidade varchar2(20),
    constraint pk_regiao primary key (id_regiao),
    constraint ck_regiao_vuln check (nivel_vulnerabilidade in ('BAIXA','MEDIA','ALTA','CRITICA'))
);

create sequence seq_regiao start with 1 increment by 1 nocache;

create table EVENTO_CLIMATICO (
    id_evento number(10) not null,
    id_regiao number(10) not null,
    tipo varchar2(40) not null,
    data_ocorrencia date not null,
    severidade varchar2(20) not null,
    descricao varchar2(4000),
    constraint pk_evento primary key (id_evento),
    constraint fk_evento_regiao foreign key (id_regiao) references REGIAO(id_regiao),
    constraint ck_evento_sev check (severidade in ('BAIXA','MEDIA','ALTA','CRITICA'))
);

create sequence seq_evento start with 1 increment by 1 nocache;

create table SENSOR (
    id_sensor number(10) not null,
    id_regiao number(10) not null,
    modelo varchar2(60),
    tipo varchar2(40),
    data_instalacao date,
    status varchar2(20) default 'ATIVO',
    constraint pk_sensor primary key (id_sensor),
    constraint fk_sensor_regiao foreign key (id_regiao) references REGIAO(id_regiao),
    constraint ck_sensor_status check (status in ('ATIVO','INATIVO','MANUTENCAO'))
);

create sequence seq_sensor start with 1 increment by 1 nocache;

create table DADO_METEOROLOGICO (
    id_dado number(10) not null,
    id_sensor number(10) not null,
    data_hora timestamp not null,
    temperatura number(5,2),
    umidade number(5,2),
    pluviosidade number(6,2),
    vento number(5,2),
    pressao number(6,2),
    constraint pk_dado primary key (id_dado),
    constraint fk_dado_sensor foreign key (id_sensor) references SENSOR(id_sensor)
);

create sequence seq_dado start with 1 increment by 1 nocache;

create table PREVISAO (
    id_previsao number(10) not null,
    id_regiao number(10) not null,
    data_geracao timestamp not null,
    tipo_risco varchar2(40) not null,
    probabilidade number(5,2),
    nivel_risco varchar2(20),
    constraint pk_previsao primary key (id_previsao),
    constraint fk_previsao_regiao foreign key (id_regiao) references REGIAO(id_regiao),
    constraint ck_previsao_nivel check (nivel_risco in ('BAIXO','MEDIO','ALTO','CRITICO')),
    constraint ck_previsao_prob check (probabilidade between 0 and 100)
);

create sequence seq_previsao start with 1 increment by 1 nocache;

create table ORGAO_RESPONSAVEL (
    id_orgao number(10) not null,
    nome varchar2(120) not null,
    tipo varchar2(40),
    esfera varchar2(20),
    contato varchar2(120),
    constraint pk_orgao primary key (id_orgao),
    constraint ck_orgao_esfera check (esfera in ('MUNICIPAL','ESTADUAL','FEDERAL'))
);

create sequence seq_orgao start with 1 increment by 1 nocache;

create table ALERTA (
    id_alerta number(10) not null,
    id_previsao number(10) not null,
    id_orgao number(10) not null,
    data_emissao timestamp not null,
    mensagem varchar2(4000) not null,
    nivel varchar2(20) not null,
    constraint pk_alerta primary key (id_alerta),
    constraint fk_alerta_previsao foreign key (id_previsao) references PREVISAO(id_previsao),
    constraint fk_alerta_orgao foreign key (id_orgao) references ORGAO_RESPONSAVEL(id_orgao),
    constraint ck_alerta_nivel check (nivel in ('BAIXO','MEDIO','ALTO','CRITICO'))
);

create sequence seq_alerta start with 1 increment by 1 nocache;

create table IMPACTO (
    id_impacto number(10) not null,
    type_impacto varchar2(40) not null,
    descricao varchar2(4000),
    unidade_medida varchar2(20),
    constraint pk_impacto primary key (id_impacto)
);

create sequence seq_impacto start with 1 increment by 1 nocache;

-- Tabela associativa do N p N
create table EVENTO_IMPACTO (
    id_evento number(10) not null,
    id_impacto number(10) not null,
    quantidade number(12,2),
    observacao varchar2(4000),
    constraint pk_evento_impacto primary key (id_evento, id_impacto),
    constraint fk_ei_evento foreign key (id_evento) references EVENTO_CLIMATICO(id_evento),
    constraint fk_ei_impacto foreign key (id_impacto) references IMPACTO(id_impacto)
);

create table USUARIO (
    id_usuario number(10) not null,
    id_orgao number(10) not null,
    nome varchar2(120) not null,
    email varchar2(120) not null,
    senha_hash varchar2(255) not null,
    nivel_acesso varchar2(20) not null,
    constraint pk_usuario primary key (id_usuario),
    constraint uk_usuario_email unique (email),
    constraint fk_usuario_orgao foreign key (id_orgao) references ORGAO_RESPONSAVEL(id_orgao),
    constraint ck_usuario_nivel check (nivel_acesso in ('OPERADOR','GESTOR','ADMINISTRADOR'))
);

create sequence seq_usuario start with 1 increment by 1 nocache;

create table ACAO_PREVENTIVA (
    id_acao number(10) not null,
    id_alerta number(10) not null,
    descricao varchar2(4000) not null,
    data_execucao date,
    status varchar2(20),
    responsavel varchar2(120),
    constraint pk_acao primary key (id_acao),
    constraint fk_acao_alerta foreign key (id_alerta) references ALERTA(id_alerta),
    constraint ck_acao_status check (status in ('PLANEJADA','EM_EXECUCAO','CONCLUIDA','CANCELADA'))
);

create sequence seq_acao start with 1 increment by 1 nocache;

-- Outra associativa N p N
create table PREVISAO_DADO (
    id_previsao number(10) not null,
    id_dado number(10) not null,
    peso_uso number(5,2),
    constraint pk_previsao_dado primary key (id_previsao, id_dado),
    constraint fk_pd_previsao foreign key (id_previsao) references PREVISAO(id_previsao),
    constraint fk_pd_dado foreign key (id_dado) references DADO_METEOROLOGICO(id_dado)
);


-- Inserts para testar o banco (DML)

-- Regioes
insert into REGIAO values (seq_regiao.nextval, 'Petrópolis - Centro', 'RJ', 'ENCOSTA', -22.505000, -43.178000, 'CRITICA');
insert into REGIAO values (seq_regiao.nextval, 'São Paulo - Zona Leste', 'SP', 'PLANICIE', -23.540000, -46.460000, 'ALTA');
insert into REGIAO values (seq_regiao.nextval, 'Recife - Boa Viagem', 'PE', 'LITORAL', -8.118000, -34.901000, 'ALTA');
insert into REGIAO values (seq_regiao.nextval, 'Blumenau - Vale', 'SC', 'VALE', -26.919000, -49.066000, 'CRITICA');

-- Orgaos
insert into ORGAO_RESPONSAVEL values (seq_orgao.nextval, 'Defesa Civil RJ', 'DEFESA_CIVIL', 'ESTADUAL', 'defesacivil@rj.gov.br');
insert into ORGAO_RESPONSAVEL values (seq_orgao.nextval, 'Prefeitura SP', 'PREFEITURA', 'MUNICIPAL', 'protecao@sp.gov.br');
insert into ORGAO_RESPONSAVEL values (seq_orgao.nextval, 'INMET', 'INSTITUTO', 'FEDERAL', 'contato@inmet.gov.br');

-- Sensores
insert into SENSOR values (seq_sensor.nextval, 1, 'Davis Vantage Pro2', 'PLUVIOMETRO', to_date('2024-01-15','YYYY-MM-DD'), 'ATIVO');
insert into SENSOR values (seq_sensor.nextval, 1, 'WS-2000', 'ESTACAO_COMPLETA', to_date('2024-03-10','YYYY-MM-DD'), 'ATIVO');
insert into SENSOR values (seq_sensor.nextval, 2, 'Vaisala WXT536', 'ANEMOMETRO', to_date('2024-05-22','YYYY-MM-DD'), 'ATIVO');
insert into SENSOR values (seq_sensor.nextval, 4, 'Hobo RX3000', 'ESTACAO_COMPLETA', to_date('2024-07-05','YYYY-MM-DD'), 'ATIVO');

-- Eventos
insert into EVENTO_CLIMATICO values (seq_evento.nextval, 1, 'DESLIZAMENTO', to_date('2024-02-15','YYYY-MM-DD'), 'CRITICA', 'Desabamento de encosta por conta de chuva forte');
insert into EVENTO_CLIMATICO values (seq_evento.nextval, 2, 'ENCHENTE', to_date('2024-03-20','YYYY-MM-DD'), 'ALTA', 'Alagamento forte nas avenidas principais da ZL');
insert into EVENTO_CLIMATICO values (seq_evento.nextval, 4, 'ENCHENTE', to_date('2025-01-08','YYYY-MM-DD'), 'CRITICA', 'Rio Itajai subiu demais e transbordou');

-- Impactos
insert into IMPACTO values (seq_impacto.nextval, 'VITIMAS', 'Qtd de mortes confirmadas', 'pessoas');
insert into IMPACTO values (seq_impacto.nextval, 'DESABRIGADOS', 'Gente que perdeu a casa e ta em abrigo', 'pessoas');
insert into IMPACTO values (seq_impacto.nextval, 'FINANCEIRO', 'Prejuizo em dinheiro estimado', 'BRL');
insert into IMPACTO values (seq_impacto.nextval, 'ESTRUTURAL', 'Casas e predios quebrados ou condenados', 'unidades');

-- Relacionamento Evento x Impacto
insert into EVENTO_IMPACTO values (1, 1, 12.00, 'Tristeza, obitos confirmados no local');
insert into EVENTO_IMPACTO values (1, 2, 350.00, 'Muita gente desabrigada nas escolas municipais');
insert into EVENTO_IMPACTO values (1, 3, 5000000.00, 'Custo alto para reconstruir a pista');
insert into EVENTO_IMPACTO values (2, 2, 180.00, 'Desalojados levados para o ginásio');
insert into EVENTO_IMPACTO values (2, 4, 75.00, 'Comercio local bem destruido');
insert into EVENTO_IMPACTO values (3, 1, 4.00, 'Mortes por arrastamento');
insert into EVENTO_IMPACTO values (3, 3, 12000000.00, 'Prejuizo gigante na cidade toda');

-- Dados meteorologicos inseridos com timestamp estruturado manualmente
insert into DADO_METEOROLOGICO values (seq_dado.nextval, 1, to_timestamp('2024-02-14 18:00:00', 'YYYY-MM-DD HH24:MI:SS'), 24.50, 92.00, 85.50, 15.20, 1010.50);
insert into DADO_METEOROLOGICO values (seq_dado.nextval, 1, to_timestamp('2024-02-14 23:00:00', 'YYYY-MM-DD HH24:MI:SS'), 22.00, 96.00, 120.80, 22.40, 1008.20);
insert into DADO_METEOROLOGICO values (seq_dado.nextval, 2, to_timestamp('2024-02-15 02:00:00', 'YYYY-MM-DD HH24:MI:SS'), 21.50, 98.00, 145.20, 28.00, 1006.00);
insert into DADO_METEOROLOGICO values (seq_dado.nextval, 4, to_timestamp('2025-01-07 14:00:00', 'YYYY-MM-DD HH24:MI:SS'), 26.00, 88.00, 95.00, 18.50, 1009.00);
insert into DADO_METEOROLOGICO values (seq_dado.nextval, 4, to_timestamp('2025-01-07 20:00:00', 'YYYY-MM-DD HH24:MI:SS'), 24.00, 95.00, 165.30, 25.00, 1005.50);

-- Previsoes
insert into PREVISAO values (seq_previsao.nextval, 1, to_timestamp('2024-02-14 12:00:00', 'YYYY-MM-DD HH24:MI:SS'), 'DESLIZAMENTO', 87.50, 'CRITICO');
insert into PREVISAO values (seq_previsao.nextval, 4, to_timestamp('2025-01-07 10:00:00', 'YYYY-MM-DD HH24:MI:SS'), 'ENCHENTE', 92.00, 'CRITICO');
insert into PREVISAO values (seq_previsao.nextval, 2, to_timestamp('2025-06-01 09:00:00', 'YYYY-MM-DD HH24:MI:SS'), 'ENCHENTE', 65.00, 'ALTO');

-- Vinculo Previsao x Dado
insert into PREVISAO_DADO values (1, 1, 0.30);
insert into PREVISAO_DADO values (1, 2, 0.35);
insert into PREVISAO_DADO values (1, 3, 0.35);
insert into PREVISAO_DADO values (2, 4, 0.45);
insert into PREVISAO_DADO values (2, 5, 0.55);

-- Alertas emitidos
insert into ALERTA values (seq_alerta.nextval, 1, 1, to_timestamp('2024-02-14 13:00:00', 'YYYY-MM-DD HH24:MI:SS'), 'Perigo de deslizamento em Petropolis! Saiam de casa imediatamente.', 'CRITICO');
insert into ALERTA values (seq_alerta.nextval, 2, 1, to_timestamp('2025-01-07 11:00:00', 'YYYY-MM-DD HH24:MI:SS'), 'Alerta maximo de enchente vindo ai no Vale do Itajai.', 'CRITICO');
insert into ALERTA values (seq_alerta.nextval, 3, 2, to_timestamp('2025-06-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS'), 'Chuva forte prevista para as proximas horas na Zona Leste.', 'ALTO');

-- Usuarios do sistema
insert into USUARIO values (seq_usuario.nextval, 1, 'Ana Souza', 'ana.souza@defesacivil.rj.gov.br', 'hash_senha_123', 'GESTOR');
insert into USUARIO values (seq_usuario.nextval, 2, 'Carlos Lima', 'carlos.lima@sp.gov.br', 'hash_senha_456', 'OPERADOR');
insert into USUARIO values (seq_usuario.nextval, 3, 'Mariana Alves', 'mariana@inmet.gov.br', 'hash_senha_789', 'ADMINISTRADOR');

-- Acoes preventivas tomadas
insert into ACAO_PREVENTIVA values (seq_acao.nextval, 1, 'Tirar moradores das encostas perigosas antes de cair tudo', to_date('2024-02-14','YYYY-MM-DD'), 'CONCLUIDA', 'Defesa Civil RJ');
insert into ACAO_PREVENTIVA values (seq_acao.nextval, 2, 'Ligar sirenes de aviso e abrir escolas para abrigo', to_date('2025-01-07','YYYY-MM-DD'), 'CONCLUIDA', 'Defesa Civil SC');
insert into ACAO_PREVENTIVA values (seq_acao.nextval, 3, 'Avisar midia e colocar equipes na rua de plantao', to_date('2025-06-01','YYYY-MM-DD'), 'EM_EXECUCAO', 'Prefeitura SP');

commit;


-- Consultas para testar se os joins funcionam (Selects)

-- 1) Ver o historico dos eventos e onde aconteceram
select r.nome as nome_regiao, r.estado, e.tipo, e.severidade, e.data_ocorrencia
from REGIAO r
join EVENTO_CLIMATICO e on e.id_regiao = r.id_regiao
order by e.data_ocorrencia desc;

-- 2) Ver o estrago/impacto de cada evento cadastrado
select e.id_evento, e.tipo, i.type_impacto, ei.quantidade, i.unidade_medida
from EVENTO_CLIMATICO e
join EVENTO_IMPACTO ei on ei.id_evento = e.id_evento
join IMPACTO i on i.id_impacto = ei.id_impacto
order by e.id_evento;

-- 3) Mostrar alertas criticos e quem eh o orgao responsavel
select a.id_alerta, a.nivel, a.data_emissao, o.nome as nome_orgao, p.tipo_risco
from ALERTA a
join ORGAO_RESPONSAVEL o on o.id_orgao = a.id_orgao
join PREVISAO p on p.id_previsao = a.id_previsao
where a.nivel = 'CRITICO'
order by a.data_emissao desc;

-- 4) Agrupamento para ver total de problemas por regiao
select r.nome as regiao, e.tipo, count(*) as total
from REGIAO r
join EVENTO_CLIMATICO e on e.id_regiao = r.id_regiao
group by r.nome, e.tipo
order by total desc;

-- 5) Ver as acoes preventivas de alertas que eram perigosos (Alto ou Critico)
select ac.descricao, ac.status, ac.data_execucao, a.nivel
from ACAO_PREVENTIVA ac
join ALERTA a on a.id_alerta = ac.id_alerta
where a.nivel in ('ALTO','CRITICO')
order by ac.data_execucao desc;
