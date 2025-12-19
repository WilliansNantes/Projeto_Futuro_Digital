--
-- PostgreSQL database dump
--

-- Dumped from database version 16.1
-- Dumped by pg_dump version 16.1

-- Started on 2025-12-19 17:07:13

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
-- TOC entry 216 (class 1259 OID 40969)
-- Name: fornecedor_empresa; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.fornecedor_empresa (
    name_company character varying(100),
    email_company character varying(100),
    contato character varying(11),
    cidade character varying(100),
    "id_companY" integer NOT NULL,
    status_id integer
);


ALTER TABLE public.fornecedor_empresa OWNER TO postgres;

--
-- TOC entry 224 (class 1259 OID 49235)
-- Name: leads; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.leads (
    id_lead integer NOT NULL,
    nome character varying,
    email character varying(100),
    contato numeric,
    cidade character varying(20),
    score numeric,
    status_id integer,
    "valor KW/H mes 01" numeric,
    "Valor KW/H mes 02" numeric,
    "Valor KW/H mes 03" numeric,
    "Media KW/H por mes" numeric,
    "Media pago/mes" numeric
);


ALTER TABLE public.leads OWNER TO postgres;

--
-- TOC entry 223 (class 1259 OID 49234)
-- Name: leads_id_leads_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.leads_id_leads_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.leads_id_leads_seq OWNER TO postgres;

--
-- TOC entry 4841 (class 0 OID 0)
-- Dependencies: 223
-- Name: leads_id_leads_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.leads_id_leads_seq OWNED BY public.leads.id_lead;


--
-- TOC entry 218 (class 1259 OID 41004)
-- Name: ordem; Type: TABLE; Schema: public; Owner: postgres
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


ALTER TABLE public.ordem OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 49161)
-- Name: order_id_order_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.order_id_order_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.order_id_order_seq OWNER TO postgres;

--
-- TOC entry 4842 (class 0 OID 0)
-- Dependencies: 219
-- Name: order_id_order_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.order_id_order_seq OWNED BY public.ordem.id_ordem;


--
-- TOC entry 217 (class 1259 OID 40976)
-- Name: produtos; Type: TABLE; Schema: public; Owner: postgres
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


ALTER TABLE public.produtos OWNER TO postgres;

--
-- TOC entry 220 (class 1259 OID 49170)
-- Name: products_id_product_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.products_id_product_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.products_id_product_seq OWNER TO postgres;

--
-- TOC entry 4843 (class 0 OID 0)
-- Dependencies: 220
-- Name: products_id_product_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.products_id_product_seq OWNED BY public.produtos.id_produto;


--
-- TOC entry 226 (class 1259 OID 49244)
-- Name: status; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.status (
    id_status integer NOT NULL,
    "situação" character varying,
    score_min numeric,
    score_max numeric
);


ALTER TABLE public.status OWNER TO postgres;

--
-- TOC entry 225 (class 1259 OID 49243)
-- Name: status_id_status_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.status_id_status_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.status_id_status_seq OWNER TO postgres;

--
-- TOC entry 4844 (class 0 OID 0)
-- Dependencies: 225
-- Name: status_id_status_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.status_id_status_seq OWNED BY public.status.id_status;


--
-- TOC entry 221 (class 1259 OID 49179)
-- Name: supplier_company_id_companY_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."supplier_company_id_companY_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."supplier_company_id_companY_seq" OWNER TO postgres;

--
-- TOC entry 4845 (class 0 OID 0)
-- Dependencies: 221
-- Name: supplier_company_id_companY_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."supplier_company_id_companY_seq" OWNED BY public.fornecedor_empresa."id_companY";


--
-- TOC entry 215 (class 1259 OID 40962)
-- Name: usuario; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.usuario (
    nome_user character varying(100),
    email character varying(100),
    password character varying(10),
    funcao character varying,
    id_user integer NOT NULL
);


ALTER TABLE public.usuario OWNER TO postgres;

--
-- TOC entry 222 (class 1259 OID 49188)
-- Name: user_id_user_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.user_id_user_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.user_id_user_seq OWNER TO postgres;

--
-- TOC entry 4846 (class 0 OID 0)
-- Dependencies: 222
-- Name: user_id_user_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.user_id_user_seq OWNED BY public.usuario.id_user;


--
-- TOC entry 4660 (class 2604 OID 49180)
-- Name: fornecedor_empresa id_companY; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fornecedor_empresa ALTER COLUMN "id_companY" SET DEFAULT nextval('public."supplier_company_id_companY_seq"'::regclass);


--
-- TOC entry 4663 (class 2604 OID 49238)
-- Name: leads id_lead; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.leads ALTER COLUMN id_lead SET DEFAULT nextval('public.leads_id_leads_seq'::regclass);


--
-- TOC entry 4662 (class 2604 OID 49162)
-- Name: ordem id_ordem; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ordem ALTER COLUMN id_ordem SET DEFAULT nextval('public.order_id_order_seq'::regclass);


--
-- TOC entry 4661 (class 2604 OID 49171)
-- Name: produtos id_produto; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.produtos ALTER COLUMN id_produto SET DEFAULT nextval('public.products_id_product_seq'::regclass);


--
-- TOC entry 4664 (class 2604 OID 49247)
-- Name: status id_status; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.status ALTER COLUMN id_status SET DEFAULT nextval('public.status_id_status_seq'::regclass);


--
-- TOC entry 4659 (class 2604 OID 49189)
-- Name: usuario id_user; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuario ALTER COLUMN id_user SET DEFAULT nextval('public.user_id_user_seq'::regclass);


--
-- TOC entry 4825 (class 0 OID 40969)
-- Dependencies: 216
-- Data for Name: fornecedor_empresa; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.fornecedor_empresa (name_company, email_company, contato, cidade, "id_companY", status_id) VALUES ('Placa Brasil', 'placabrasil@gmail.com', '34784707', 'São Paulo', 1, 4);
INSERT INTO public.fornecedor_empresa (name_company, email_company, contato, cidade, "id_companY", status_id) VALUES ('Ferramenta Gerais', 'ferramentas gerrais@gmail.com', '34754459', 'Porto Alegre', 2, 4);
INSERT INTO public.fornecedor_empresa (name_company, email_company, contato, cidade, "id_companY", status_id) VALUES ('ManoBras', 'manobras.f@email.com', '34751558', 'Canoas', 3, 5);


--
-- TOC entry 4833 (class 0 OID 49235)
-- Dependencies: 224
-- Data for Name: leads; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.leads (id_lead, nome, email, contato, cidade, score, status_id, "valor KW/H mes 01", "Valor KW/H mes 02", "Valor KW/H mes 03", "Media KW/H por mes", "Media pago/mes") VALUES (1, 'willians Nantes', 'will.nantes@gmail.com', 51993546495, 'canoas', 0, 1, 205, 186, 218, NULL, NULL);


--
-- TOC entry 4827 (class 0 OID 41004)
-- Dependencies: 218
-- Data for Name: ordem; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.ordem (lead_id, data_ordem, produto_id, quantidade, valor_vendido, id_ordem, status) VALUES (1, '2025-08-12', 1, 3, 1605, 1, 6);


--
-- TOC entry 4826 (class 0 OID 40976)
-- Dependencies: 217
-- Data for Name: produtos; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.produtos (nome_produto, "valor _por_und", qtd_comprado, qtd_vendido, qtd_in_stock, id_produto, fornecedor_id) VALUES ('Placa Solar 700w', 535.00, 5, 3, 2, 1, 1);


--
-- TOC entry 4835 (class 0 OID 49244)
-- Dependencies: 226
-- Data for Name: status; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.status (id_status, "situação", score_min, score_max) VALUES (1, 'lead', 0, 50);
INSERT INTO public.status (id_status, "situação", score_min, score_max) VALUES (2, 'client01', 50, 70);
INSERT INTO public.status (id_status, "situação", score_min, score_max) VALUES (3, 'client02', 70, 100);
INSERT INTO public.status (id_status, "situação", score_min, score_max) VALUES (4, 'active', 50, 100);
INSERT INTO public.status (id_status, "situação", score_min, score_max) VALUES (5, 'inactive', 0, 100);
INSERT INTO public.status (id_status, "situação", score_min, score_max) VALUES (6, 'processing', NULL, NULL);
INSERT INTO public.status (id_status, "situação", score_min, score_max) VALUES (7, 'delivered', NULL, NULL);


--
-- TOC entry 4824 (class 0 OID 40962)
-- Dependencies: 215
-- Data for Name: usuario; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.usuario (nome_user, email, password, funcao, id_user) VALUES ('Jorge Bica', 'J.bica@gmail.com', 'jorge123', 'vendedor', 1);
INSERT INTO public.usuario (nome_user, email, password, funcao, id_user) VALUES ('Jessica Senna', 'jessica.10@gmail.com', 'jessica123', 'vendedor', 2);


--
-- TOC entry 4847 (class 0 OID 0)
-- Dependencies: 223
-- Name: leads_id_leads_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.leads_id_leads_seq', 1, true);


--
-- TOC entry 4848 (class 0 OID 0)
-- Dependencies: 219
-- Name: order_id_order_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.order_id_order_seq', 1, true);


--
-- TOC entry 4849 (class 0 OID 0)
-- Dependencies: 220
-- Name: products_id_product_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.products_id_product_seq', 1, true);


--
-- TOC entry 4850 (class 0 OID 0)
-- Dependencies: 225
-- Name: status_id_status_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.status_id_status_seq', 7, true);


--
-- TOC entry 4851 (class 0 OID 0)
-- Dependencies: 221
-- Name: supplier_company_id_companY_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."supplier_company_id_companY_seq"', 3, true);


--
-- TOC entry 4852 (class 0 OID 0)
-- Dependencies: 222
-- Name: user_id_user_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_id_user_seq', 2, true);


--
-- TOC entry 4672 (class 2606 OID 57352)
-- Name: leads leads_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.leads
    ADD CONSTRAINT leads_pkey PRIMARY KEY (id_lead);


--
-- TOC entry 4670 (class 2606 OID 49178)
-- Name: produtos products_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.produtos
    ADD CONSTRAINT products_pkey PRIMARY KEY (id_produto);


--
-- TOC entry 4674 (class 2606 OID 49251)
-- Name: status status_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.status
    ADD CONSTRAINT status_pkey PRIMARY KEY (id_status);


--
-- TOC entry 4668 (class 2606 OID 49187)
-- Name: fornecedor_empresa supplier_company_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fornecedor_empresa
    ADD CONSTRAINT supplier_company_pkey PRIMARY KEY ("id_companY");


--
-- TOC entry 4666 (class 2606 OID 49196)
-- Name: usuario user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuario
    ADD CONSTRAINT user_pkey PRIMARY KEY (id_user);


--
-- TOC entry 4680 (class 2606 OID 57346)
-- Name: leads leads_status_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.leads
    ADD CONSTRAINT leads_status_id_fkey FOREIGN KEY (status_id) REFERENCES public.status(id_status) NOT VALID;


--
-- TOC entry 4677 (class 2606 OID 57363)
-- Name: ordem ordem_lead_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ordem
    ADD CONSTRAINT ordem_lead_id_fkey FOREIGN KEY (lead_id) REFERENCES public.leads(id_lead) NOT VALID;


--
-- TOC entry 4678 (class 2606 OID 57353)
-- Name: ordem ordem_produto_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ordem
    ADD CONSTRAINT ordem_produto_id_fkey FOREIGN KEY (produto_id) REFERENCES public.produtos(id_produto) NOT VALID;


--
-- TOC entry 4679 (class 2606 OID 57358)
-- Name: ordem ordem_status_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ordem
    ADD CONSTRAINT ordem_status_fkey FOREIGN KEY (status) REFERENCES public.status(id_status) NOT VALID;


--
-- TOC entry 4675 (class 2606 OID 57373)
-- Name: produtos produtos_fornecedor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.produtos
    ADD CONSTRAINT produtos_fornecedor_id_fkey FOREIGN KEY (fornecedor_id) REFERENCES public.fornecedor_empresa("id_companY") NOT VALID;


--
-- TOC entry 4676 (class 2606 OID 57368)
-- Name: produtos produtos_id_produto_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.produtos
    ADD CONSTRAINT produtos_id_produto_fkey FOREIGN KEY (id_produto) REFERENCES public.produtos(id_produto) NOT VALID;


-- Completed on 2025-12-19 17:07:13

--
-- PostgreSQL database dump complete
--

