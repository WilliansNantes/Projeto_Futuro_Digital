--
-- PostgreSQL database dump
--

-- Dumped from database version 16.1
-- Dumped by pg_dump version 16.1

-- Started on 2026-03-03 11:39:54

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 228 (class 1259 OID 65539)
-- Name: consumo; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.consumo (
    id_consumo bigint NOT NULL,
    ano numeric(4,0),
    mes numeric(2,0),
    valor_consumo numeric,
    pessoa_id integer
);


--
-- TOC entry 227 (class 1259 OID 65538)
-- Name: consumo_id_consumo_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.consumo_id_consumo_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 4852 (class 0 OID 0)
-- Dependencies: 227
-- Name: consumo_id_consumo_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.consumo_id_consumo_seq OWNED BY public.consumo.id_consumo;


--
-- TOC entry 216 (class 1259 OID 40969)
-- Name: fornecedor_empresa; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.fornecedor_empresa (
    name_company character varying(100),
    email_company character varying(100),
    contato character varying(11),
    cidade character varying(100),
    id_company integer NOT NULL,
    status_id integer
);


--
-- TOC entry 224 (class 1259 OID 49235)
-- Name: pessoas; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.pessoas (
    id_pessoa integer NOT NULL,
    nome character varying,
    email character varying(100),
    contato numeric,
    cidade character varying(20),
    status_id integer,
    media_cons_mes numeric,
    score numeric
);


--
-- TOC entry 223 (class 1259 OID 49234)
-- Name: leads_id_leads_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.leads_id_leads_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 4853 (class 0 OID 0)
-- Dependencies: 223
-- Name: leads_id_leads_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.leads_id_leads_seq OWNED BY public.pessoas.id_pessoa;


--
-- TOC entry 218 (class 1259 OID 41004)
-- Name: ordem; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ordem (
    lead_id integer NOT NULL,
    data_ordem date,
    produto_id integer NOT NULL,
    quantidade numeric,
    valor_vendido numeric,
    id_ordem integer NOT NULL,
    status integer NOT NULL
);


--
-- TOC entry 219 (class 1259 OID 49161)
-- Name: order_id_order_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.order_id_order_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 4854 (class 0 OID 0)
-- Dependencies: 219
-- Name: order_id_order_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.order_id_order_seq OWNED BY public.ordem.id_ordem;


--
-- TOC entry 217 (class 1259 OID 40976)
-- Name: produtos; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.produtos (
    nome_produto character varying(100),
    "valor _por_und" numeric(10,2),
    qtd_comprado numeric,
    qtd_vendido numeric,
    qtd_in_stock numeric,
    id_produto integer NOT NULL,
    fornecedor_id integer
);


--
-- TOC entry 220 (class 1259 OID 49170)
-- Name: products_id_product_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.products_id_product_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 4855 (class 0 OID 0)
-- Dependencies: 220
-- Name: products_id_product_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.products_id_product_seq OWNED BY public.produtos.id_produto;


--
-- TOC entry 226 (class 1259 OID 49244)
-- Name: status; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.status (
    id_status integer NOT NULL,
    "situação" character varying,
    score_min numeric,
    score_max numeric
);


--
-- TOC entry 225 (class 1259 OID 49243)
-- Name: status_id_status_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.status_id_status_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 4856 (class 0 OID 0)
-- Dependencies: 225
-- Name: status_id_status_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.status_id_status_seq OWNED BY public.status.id_status;


--
-- TOC entry 221 (class 1259 OID 49179)
-- Name: supplier_company_id_companY_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."supplier_company_id_companY_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 4857 (class 0 OID 0)
-- Dependencies: 221
-- Name: supplier_company_id_companY_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."supplier_company_id_companY_seq" OWNED BY public.fornecedor_empresa.id_company;


--
-- TOC entry 215 (class 1259 OID 40962)
-- Name: usuario; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.usuario (
    nome_user character varying(100),
    email character varying(100),
    password character varying(10),
    funcao character varying,
    id_user integer NOT NULL
);


--
-- TOC entry 222 (class 1259 OID 49188)
-- Name: user_id_user_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.user_id_user_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 4858 (class 0 OID 0)
-- Dependencies: 222
-- Name: user_id_user_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.user_id_user_seq OWNED BY public.usuario.id_user;


--
-- TOC entry 4670 (class 2604 OID 65542)
-- Name: consumo id_consumo; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.consumo ALTER COLUMN id_consumo SET DEFAULT nextval('public.consumo_id_consumo_seq'::regclass);


--
-- TOC entry 4665 (class 2604 OID 49180)
-- Name: fornecedor_empresa id_company; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.fornecedor_empresa ALTER COLUMN id_company SET DEFAULT nextval('public."supplier_company_id_companY_seq"'::regclass);


--
-- TOC entry 4667 (class 2604 OID 49162)
-- Name: ordem id_ordem; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ordem ALTER COLUMN id_ordem SET DEFAULT nextval('public.order_id_order_seq'::regclass);


--
-- TOC entry 4668 (class 2604 OID 49238)
-- Name: pessoas id_pessoa; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pessoas ALTER COLUMN id_pessoa SET DEFAULT nextval('public.leads_id_leads_seq'::regclass);


--
-- TOC entry 4666 (class 2604 OID 49171)
-- Name: produtos id_produto; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.produtos ALTER COLUMN id_produto SET DEFAULT nextval('public.products_id_product_seq'::regclass);


--
-- TOC entry 4669 (class 2604 OID 49247)
-- Name: status id_status; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.status ALTER COLUMN id_status SET DEFAULT nextval('public.status_id_status_seq'::regclass);


--
-- TOC entry 4664 (class 2604 OID 49189)
-- Name: usuario id_user; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.usuario ALTER COLUMN id_user SET DEFAULT nextval('public.user_id_user_seq'::regclass);


--
-- TOC entry 4846 (class 0 OID 65539)
-- Dependencies: 228
-- Data for Name: consumo; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.consumo (id_consumo, ano, mes, valor_consumo, pessoa_id) VALUES (1, 2025, 1, 238.0, 8);
INSERT INTO public.consumo (id_consumo, ano, mes, valor_consumo, pessoa_id) VALUES (3, 2025, 3, 227.0, 8);
INSERT INTO public.consumo (id_consumo, ano, mes, valor_consumo, pessoa_id) VALUES (2, 2025, 2, 250.0, 8);


--
-- TOC entry 4834 (class 0 OID 40969)
-- Dependencies: 216
-- Data for Name: fornecedor_empresa; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.fornecedor_empresa (name_company, email_company, contato, cidade, id_company, status_id) VALUES ('Placa Brasil', 'placabrasil@gmail.com', '34784707', 'São Paulo', 1, 4);
INSERT INTO public.fornecedor_empresa (name_company, email_company, contato, cidade, id_company, status_id) VALUES ('Ferramenta Gerais', 'ferramentas gerrais@gmail.com', '34754459', 'Porto Alegre', 2, 4);
INSERT INTO public.fornecedor_empresa (name_company, email_company, contato, cidade, id_company, status_id) VALUES ('ManoBras', 'manobras.f@email.com', '34751558', 'Canoas', 3, 5);
INSERT INTO public.fornecedor_empresa (name_company, email_company, contato, cidade, id_company, status_id) VALUES ('PlacasEnergias', 'placasenergias@email.com', '981653456', 'São Paulo', 4, 4);
INSERT INTO public.fornecedor_empresa (name_company, email_company, contato, cidade, id_company, status_id) VALUES ('PlastSul Filial', 'plastsul@email.com', '5123456237', 'Porto Alegre', 5, 4);


--
-- TOC entry 4836 (class 0 OID 41004)
-- Dependencies: 218
-- Data for Name: ordem; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.ordem (lead_id, data_ordem, produto_id, quantidade, valor_vendido, id_ordem, status) VALUES (1, '2025-08-12', 1, 3, 1605, 1, 6);
INSERT INTO public.ordem (lead_id, data_ordem, produto_id, quantidade, valor_vendido, id_ordem, status) VALUES (1, '2026-01-21', 1, 2, 2845.25, 4, 6);


--
-- TOC entry 4842 (class 0 OID 49235)
-- Dependencies: 224
-- Data for Name: pessoas; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.pessoas (id_pessoa, nome, email, contato, cidade, status_id, media_cons_mes, score) VALUES (1, 'willians Nantes', 'will.nantes@gmail.com', 51993546495, 'canoas', 1, NULL, NULL);
INSERT INTO public.pessoas (id_pessoa, nome, email, contato, cidade, status_id, media_cons_mes, score) VALUES (5, 'Jorge Nantes', 'jorgenantes@email.com', 51992625879, NULL, 1, NULL, NULL);
INSERT INTO public.pessoas (id_pessoa, nome, email, contato, cidade, status_id, media_cons_mes, score) VALUES (6, 'Ruberval Santos', 'rebersantos@email.com', 5134754459, NULL, 1, NULL, NULL);
INSERT INTO public.pessoas (id_pessoa, nome, email, contato, cidade, status_id, media_cons_mes, score) VALUES (7, 'Persival Santos', 'persivalsantos@email.com', 5134757859, 'Porto Alegre', 1, NULL, NULL);
INSERT INTO public.pessoas (id_pessoa, nome, email, contato, cidade, status_id, media_cons_mes, score) VALUES (8, 'Maria Santos', 'mariasantos@email.com', 5134778859, 'Porto Alegre', 1, NULL, NULL);
INSERT INTO public.pessoas (id_pessoa, nome, email, contato, cidade, status_id, media_cons_mes, score) VALUES (9, 'Maria Rodrigues', 'mariarodrigues@email.com', 5134778859, 'Porto Alegre', 2, NULL, NULL);
INSERT INTO public.pessoas (id_pessoa, nome, email, contato, cidade, status_id, media_cons_mes, score) VALUES (4, 'Bjor Nantes', 'Bjornantes@email.com', 11992588769, 'Chapecó', 1, NULL, NULL);


--
-- TOC entry 4835 (class 0 OID 40976)
-- Dependencies: 217
-- Data for Name: produtos; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.produtos (nome_produto, "valor _por_und", qtd_comprado, qtd_vendido, qtd_in_stock, id_produto, fornecedor_id) VALUES ('Placa Solar 700w', 535.00, 5, 3, 2, 1, 1);


--
-- TOC entry 4844 (class 0 OID 49244)
-- Dependencies: 226
-- Data for Name: status; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.status (id_status, "situação", score_min, score_max) VALUES (1, 'lead', 0, 50);
INSERT INTO public.status (id_status, "situação", score_min, score_max) VALUES (6, 'processing', NULL, NULL);
INSERT INTO public.status (id_status, "situação", score_min, score_max) VALUES (7, 'delivered', NULL, NULL);
INSERT INTO public.status (id_status, "situação", score_min, score_max) VALUES (2, 'client01', 50, 100);
INSERT INTO public.status (id_status, "situação", score_min, score_max) VALUES (3, 'client02', 100, 150);
INSERT INTO public.status (id_status, "situação", score_min, score_max) VALUES (4, 'active', NULL, NULL);
INSERT INTO public.status (id_status, "situação", score_min, score_max) VALUES (5, 'inactive', NULL, NULL);


--
-- TOC entry 4833 (class 0 OID 40962)
-- Dependencies: 215
-- Data for Name: usuario; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.usuario (nome_user, email, password, funcao, id_user) VALUES ('Jorge Bica', 'J.bica@gmail.com', 'jorge123', 'vendedor', 1);
INSERT INTO public.usuario (nome_user, email, password, funcao, id_user) VALUES ('Jessica Senna', 'jessica.10@gmail.com', 'jessica123', 'vendedor', 2);
INSERT INTO public.usuario (nome_user, email, password, funcao, id_user) VALUES ('Lincon Meireles', 'linconemail@email.com', 'meirele123', 'Lider  de equipe', 3);
INSERT INTO public.usuario (nome_user, email, password, funcao, id_user) VALUES ('Walker Ragnar Bica Nantes', 'Ragnar@email.com', 'Walker123', 'Supervisor', 4);
INSERT INTO public.usuario (nome_user, email, password, funcao, id_user) VALUES (NULL, NULL, '525252', 'Gerente de Vendas', 5);


--
-- TOC entry 4859 (class 0 OID 0)
-- Dependencies: 227
-- Name: consumo_id_consumo_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.consumo_id_consumo_seq', 3, true);


--
-- TOC entry 4860 (class 0 OID 0)
-- Dependencies: 223
-- Name: leads_id_leads_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.leads_id_leads_seq', 9, true);


--
-- TOC entry 4861 (class 0 OID 0)
-- Dependencies: 219
-- Name: order_id_order_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.order_id_order_seq', 4, true);


--
-- TOC entry 4862 (class 0 OID 0)
-- Dependencies: 220
-- Name: products_id_product_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.products_id_product_seq', 1, true);


--
-- TOC entry 4863 (class 0 OID 0)
-- Dependencies: 225
-- Name: status_id_status_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.status_id_status_seq', 7, true);


--
-- TOC entry 4864 (class 0 OID 0)
-- Dependencies: 221
-- Name: supplier_company_id_companY_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public."supplier_company_id_companY_seq"', 5, true);


--
-- TOC entry 4865 (class 0 OID 0)
-- Dependencies: 222
-- Name: user_id_user_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.user_id_user_seq', 5, true);


--
-- TOC entry 4682 (class 2606 OID 65546)
-- Name: consumo consumo_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.consumo
    ADD CONSTRAINT consumo_pkey PRIMARY KEY (id_consumo);


--
-- TOC entry 4678 (class 2606 OID 57352)
-- Name: pessoas leads_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pessoas
    ADD CONSTRAINT leads_pkey PRIMARY KEY (id_pessoa);


--
-- TOC entry 4676 (class 2606 OID 49178)
-- Name: produtos products_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.produtos
    ADD CONSTRAINT products_pkey PRIMARY KEY (id_produto);


--
-- TOC entry 4680 (class 2606 OID 49251)
-- Name: status status_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.status
    ADD CONSTRAINT status_pkey PRIMARY KEY (id_status);


--
-- TOC entry 4674 (class 2606 OID 49187)
-- Name: fornecedor_empresa supplier_company_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.fornecedor_empresa
    ADD CONSTRAINT supplier_company_pkey PRIMARY KEY (id_company);


--
-- TOC entry 4672 (class 2606 OID 49196)
-- Name: usuario user_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.usuario
    ADD CONSTRAINT user_pkey PRIMARY KEY (id_user);


--
-- TOC entry 4689 (class 2606 OID 65547)
-- Name: consumo consumo_pessoa_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.consumo
    ADD CONSTRAINT consumo_pessoa_id_fkey FOREIGN KEY (pessoa_id) REFERENCES public.pessoas(id_pessoa);


--
-- TOC entry 4688 (class 2606 OID 57346)
-- Name: pessoas leads_status_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pessoas
    ADD CONSTRAINT leads_status_id_fkey FOREIGN KEY (status_id) REFERENCES public.status(id_status) NOT VALID;


--
-- TOC entry 4685 (class 2606 OID 57363)
-- Name: ordem ordem_lead_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ordem
    ADD CONSTRAINT ordem_lead_id_fkey FOREIGN KEY (lead_id) REFERENCES public.pessoas(id_pessoa) NOT VALID;


--
-- TOC entry 4686 (class 2606 OID 57353)
-- Name: ordem ordem_produto_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ordem
    ADD CONSTRAINT ordem_produto_id_fkey FOREIGN KEY (produto_id) REFERENCES public.produtos(id_produto) NOT VALID;


--
-- TOC entry 4687 (class 2606 OID 57358)
-- Name: ordem ordem_status_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ordem
    ADD CONSTRAINT ordem_status_fkey FOREIGN KEY (status) REFERENCES public.status(id_status) NOT VALID;


--
-- TOC entry 4683 (class 2606 OID 57373)
-- Name: produtos produtos_fornecedor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.produtos
    ADD CONSTRAINT produtos_fornecedor_id_fkey FOREIGN KEY (fornecedor_id) REFERENCES public.fornecedor_empresa(id_company) NOT VALID;


--
-- TOC entry 4684 (class 2606 OID 57368)
-- Name: produtos produtos_id_produto_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.produtos
    ADD CONSTRAINT produtos_id_produto_fkey FOREIGN KEY (id_produto) REFERENCES public.produtos(id_produto) NOT VALID;


-- Completed on 2026-03-03 11:39:55

--
-- PostgreSQL database dump complete
--

