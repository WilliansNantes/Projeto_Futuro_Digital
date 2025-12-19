--
-- PostgreSQL database dump
--

-- Dumped from database version 16.1
-- Dumped by pg_dump version 16.1

-- Started on 2025-12-19 10:22:35

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
-- TOC entry 224 (class 1259 OID 49235)
-- Name: leads; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.leads (
    id_leads integer NOT NULL,
    name character varying,
    email character varying(100),
    contacty numeric,
    city character varying(20),
    score numeric,
    status_id integer,
    "Value KW/H month 01" numeric,
    "Value KW/H month 02" numeric,
    "Value KW/H month 03" numeric,
    "Average KW/h by month" numeric,
    "Average electric bill" numeric
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
-- TOC entry 4843 (class 0 OID 0)
-- Dependencies: 223
-- Name: leads_id_leads_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.leads_id_leads_seq OWNED BY public.leads.id_leads;


--
-- TOC entry 218 (class 1259 OID 41004)
-- Name: order; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."order" (
    client_id integer NOT NULL,
    date_order date,
    product_id integer NOT NULL,
    quantaty numeric,
    sale_value numeric,
    id_order integer NOT NULL,
    status integer NOT NULL
);


ALTER TABLE public."order" OWNER TO postgres;

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
-- TOC entry 4844 (class 0 OID 0)
-- Dependencies: 219
-- Name: order_id_order_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.order_id_order_seq OWNED BY public."order".id_order;


--
-- TOC entry 217 (class 1259 OID 40976)
-- Name: products; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.products (
    name_product character varying(100),
    value_by_unit numeric(10,2),
    qty_purchased numeric,
    qty_sold numeric,
    qty_in_stock numeric,
    id_product integer NOT NULL,
    supplier_id integer
);


ALTER TABLE public.products OWNER TO postgres;

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
-- TOC entry 4845 (class 0 OID 0)
-- Dependencies: 220
-- Name: products_id_product_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.products_id_product_seq OWNED BY public.products.id_product;


--
-- TOC entry 226 (class 1259 OID 49244)
-- Name: status; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.status (
    id_status integer NOT NULL,
    situation character varying,
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
-- TOC entry 4846 (class 0 OID 0)
-- Dependencies: 225
-- Name: status_id_status_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.status_id_status_seq OWNED BY public.status.id_status;


--
-- TOC entry 216 (class 1259 OID 40969)
-- Name: supplier_company; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.supplier_company (
    name_company character varying(100),
    email_company character varying(100),
    responsible_id integer,
    contact character varying(11),
    city character varying(100),
    "id_companY" integer NOT NULL,
    status_id integer
);


ALTER TABLE public.supplier_company OWNER TO postgres;

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
-- TOC entry 4847 (class 0 OID 0)
-- Dependencies: 221
-- Name: supplier_company_id_companY_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."supplier_company_id_companY_seq" OWNED BY public.supplier_company."id_companY";


--
-- TOC entry 215 (class 1259 OID 40962)
-- Name: user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."user" (
    name_user character varying(100),
    email character varying(100),
    password character varying(10),
    function character varying,
    id_user integer NOT NULL
);


ALTER TABLE public."user" OWNER TO postgres;

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
-- TOC entry 4848 (class 0 OID 0)
-- Dependencies: 222
-- Name: user_id_user_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.user_id_user_seq OWNED BY public."user".id_user;


--
-- TOC entry 4663 (class 2604 OID 49238)
-- Name: leads id_leads; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.leads ALTER COLUMN id_leads SET DEFAULT nextval('public.leads_id_leads_seq'::regclass);


--
-- TOC entry 4662 (class 2604 OID 49162)
-- Name: order id_order; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."order" ALTER COLUMN id_order SET DEFAULT nextval('public.order_id_order_seq'::regclass);


--
-- TOC entry 4661 (class 2604 OID 49171)
-- Name: products id_product; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products ALTER COLUMN id_product SET DEFAULT nextval('public.products_id_product_seq'::regclass);


--
-- TOC entry 4664 (class 2604 OID 49247)
-- Name: status id_status; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.status ALTER COLUMN id_status SET DEFAULT nextval('public.status_id_status_seq'::regclass);


--
-- TOC entry 4660 (class 2604 OID 49180)
-- Name: supplier_company id_companY; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.supplier_company ALTER COLUMN "id_companY" SET DEFAULT nextval('public."supplier_company_id_companY_seq"'::regclass);


--
-- TOC entry 4659 (class 2604 OID 49189)
-- Name: user id_user; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user" ALTER COLUMN id_user SET DEFAULT nextval('public.user_id_user_seq'::regclass);


--
-- TOC entry 4835 (class 0 OID 49235)
-- Dependencies: 224
-- Data for Name: leads; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.leads (id_leads, name, email, contacty, city, score, status_id, "Value KW/H month 01", "Value KW/H month 02", "Value KW/H month 03", "Average KW/h by month", "Average electric bill") VALUES (1, 'willians Nantes', 'will.nantes@gmail.com', 51993546495, 'canoas', 0, 1, NULL, NULL, NULL, NULL, NULL);


--
-- TOC entry 4829 (class 0 OID 41004)
-- Dependencies: 218
-- Data for Name: order; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public."order" (client_id, date_order, product_id, quantaty, sale_value, id_order, status) VALUES (1, '2025-08-12', 1, 3, 1605, 1, 6);


--
-- TOC entry 4828 (class 0 OID 40976)
-- Dependencies: 217
-- Data for Name: products; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.products (name_product, value_by_unit, qty_purchased, qty_sold, qty_in_stock, id_product, supplier_id) VALUES ('Placa Solar 700w', 535.00, 5, 3, 2, 1, 1);


--
-- TOC entry 4837 (class 0 OID 49244)
-- Dependencies: 226
-- Data for Name: status; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.status (id_status, situation, score_min, score_max) VALUES (1, 'lead', 0, 50);
INSERT INTO public.status (id_status, situation, score_min, score_max) VALUES (2, 'client01', 50, 70);
INSERT INTO public.status (id_status, situation, score_min, score_max) VALUES (3, 'client02', 70, 100);
INSERT INTO public.status (id_status, situation, score_min, score_max) VALUES (4, 'active', 50, 100);
INSERT INTO public.status (id_status, situation, score_min, score_max) VALUES (5, 'inactive', 0, 100);
INSERT INTO public.status (id_status, situation, score_min, score_max) VALUES (6, 'processing', NULL, NULL);
INSERT INTO public.status (id_status, situation, score_min, score_max) VALUES (7, 'delivered', NULL, NULL);


--
-- TOC entry 4827 (class 0 OID 40969)
-- Dependencies: 216
-- Data for Name: supplier_company; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.supplier_company (name_company, email_company, responsible_id, contact, city, "id_companY", status_id) VALUES ('Placa Brasil', 'placabrasil@gmail.com', 2, '34784707', 'São Paulo', 1, 4);
INSERT INTO public.supplier_company (name_company, email_company, responsible_id, contact, city, "id_companY", status_id) VALUES (NULL, NULL, NULL, NULL, NULL, 2, NULL);


--
-- TOC entry 4826 (class 0 OID 40962)
-- Dependencies: 215
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public."user" (name_user, email, password, function, id_user) VALUES ('Jorge Bica', 'J.bica@gmail.com', 'jorge123', 'vendedor', 1);
INSERT INTO public."user" (name_user, email, password, function, id_user) VALUES ('Jessica Senna', 'jessica.10@gmail.com', 'jessica123', 'vendedor', 2);


--
-- TOC entry 4849 (class 0 OID 0)
-- Dependencies: 223
-- Name: leads_id_leads_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.leads_id_leads_seq', 1, true);


--
-- TOC entry 4850 (class 0 OID 0)
-- Dependencies: 219
-- Name: order_id_order_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.order_id_order_seq', 1, true);


--
-- TOC entry 4851 (class 0 OID 0)
-- Dependencies: 220
-- Name: products_id_product_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.products_id_product_seq', 1, true);


--
-- TOC entry 4852 (class 0 OID 0)
-- Dependencies: 225
-- Name: status_id_status_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.status_id_status_seq', 7, true);


--
-- TOC entry 4853 (class 0 OID 0)
-- Dependencies: 221
-- Name: supplier_company_id_companY_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."supplier_company_id_companY_seq"', 2, true);


--
-- TOC entry 4854 (class 0 OID 0)
-- Dependencies: 222
-- Name: user_id_user_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_id_user_seq', 2, true);


--
-- TOC entry 4674 (class 2606 OID 49242)
-- Name: leads leads_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.leads
    ADD CONSTRAINT leads_pkey PRIMARY KEY (id_leads);


--
-- TOC entry 4672 (class 2606 OID 49169)
-- Name: order order_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."order"
    ADD CONSTRAINT order_pkey PRIMARY KEY (id_order);


--
-- TOC entry 4670 (class 2606 OID 49178)
-- Name: products products_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_pkey PRIMARY KEY (id_product);


--
-- TOC entry 4676 (class 2606 OID 49251)
-- Name: status status_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.status
    ADD CONSTRAINT status_pkey PRIMARY KEY (id_status);


--
-- TOC entry 4668 (class 2606 OID 49187)
-- Name: supplier_company supplier_company_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.supplier_company
    ADD CONSTRAINT supplier_company_pkey PRIMARY KEY ("id_companY");


--
-- TOC entry 4666 (class 2606 OID 49196)
-- Name: user user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id_user);


--
-- TOC entry 4682 (class 2606 OID 49253)
-- Name: leads leads_status_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.leads
    ADD CONSTRAINT leads_status_id_fkey FOREIGN KEY (status_id) REFERENCES public.status(id_status) NOT VALID;


--
-- TOC entry 4680 (class 2606 OID 49202)
-- Name: order order_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."order"
    ADD CONSTRAINT order_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id_product) NOT VALID;


--
-- TOC entry 4681 (class 2606 OID 49258)
-- Name: order order_status_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."order"
    ADD CONSTRAINT order_status_fkey FOREIGN KEY (status) REFERENCES public.status(id_status) NOT VALID;


--
-- TOC entry 4679 (class 2606 OID 49222)
-- Name: products products_supplier_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_supplier_id_fkey FOREIGN KEY (supplier_id) REFERENCES public.supplier_company("id_companY") NOT VALID;


--
-- TOC entry 4677 (class 2606 OID 49227)
-- Name: supplier_company supplier_company_responsible_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.supplier_company
    ADD CONSTRAINT supplier_company_responsible_id_fkey FOREIGN KEY (responsible_id) REFERENCES public."user"(id_user) NOT VALID;


--
-- TOC entry 4678 (class 2606 OID 49263)
-- Name: supplier_company supplier_company_status_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.supplier_company
    ADD CONSTRAINT supplier_company_status_id_fkey FOREIGN KEY (status_id) REFERENCES public.status(id_status) NOT VALID;


-- Completed on 2025-12-19 10:22:35

--
-- PostgreSQL database dump complete
--

