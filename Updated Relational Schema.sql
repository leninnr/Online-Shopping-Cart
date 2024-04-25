-- This script was generated by the ERD tool in pgAdmin 4.
-- Please log an issue at https://github.com/pgadmin-org/pgadmin4/issues/new/choose if you find any bugs, including reproduction steps.

BEGIN;


CREATE TABLE IF NOT EXISTS public."Address"
(
    address_id integer NOT NULL,
    "addressLineOne" character varying COLLATE pg_catalog."default",
    "addressLineTwo" character varying COLLATE pg_catalog."default",
    state character varying COLLATE pg_catalog."default",
    country character varying COLLATE pg_catalog."default",
    zip_code integer,
    CONSTRAINT "Address_pkey" PRIMARY KEY (address_id)
);

CREATE TABLE IF NOT EXISTS public.creditcards
(
    credit_card_id serial NOT NULL,
    customer_id integer NOT NULL,
    credit_card_number character varying(16) COLLATE pg_catalog."default" NOT NULL,
    payment_address_id integer,
    card_holder_name character varying(255) COLLATE pg_catalog."default",
    expiry_date date,
    CONSTRAINT creditcards_pkey PRIMARY KEY (credit_card_id)
);

CREATE TABLE IF NOT EXISTS public.customer
(
    customer_id serial NOT NULL,
    name character varying(100) COLLATE pg_catalog."default" NOT NULL,
    balance numeric(10, 2) DEFAULT 0,
    username character varying(50) COLLATE pg_catalog."default",
    password character varying(50) COLLATE pg_catalog."default",
    cc_number character varying(255) COLLATE pg_catalog."default",
    cc_expiry date,
    cc_cvv character varying(255) COLLATE pg_catalog."default",
    CONSTRAINT customer_pkey PRIMARY KEY (customer_id),
    CONSTRAINT unique_name UNIQUE (name)
);

CREATE TABLE IF NOT EXISTS public.customer_address
(
    customer_address_id integer NOT NULL,
    customer_id integer,
    address_id integer,
    address_type character varying COLLATE pg_catalog."default",
    CONSTRAINT customer_address_pkey PRIMARY KEY (customer_address_id)
);

CREATE TABLE IF NOT EXISTS public.deliveryplans
(
    delivery_plan_id serial NOT NULL,
    order_id integer NOT NULL,
    delivery_type character varying(20) COLLATE pg_catalog."default" NOT NULL,
    delivery_price numeric(10, 2) NOT NULL,
    delivery_date date NOT NULL,
    ship_date date,
    CONSTRAINT deliveryplans_pkey PRIMARY KEY (delivery_plan_id)
);

CREATE TABLE IF NOT EXISTS public.orderitems
(
    order_item_id serial NOT NULL,
    order_id integer NOT NULL,
    product_id integer NOT NULL,
    quantity integer NOT NULL,
    CONSTRAINT orderitems_pkey PRIMARY KEY (order_item_id)
);

CREATE TABLE IF NOT EXISTS public.orders
(
    order_id serial NOT NULL,
    customer_id integer NOT NULL,
    order_status character varying(20) COLLATE pg_catalog."default" NOT NULL,
    order_date timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    credit_card_id integer,
    CONSTRAINT orders_pkey PRIMARY KEY (order_id)
);

CREATE TABLE IF NOT EXISTS public.product
(
    product_id integer NOT NULL DEFAULT nextval('products_product_id_seq'::regclass),
    name character varying(100) COLLATE pg_catalog."default" NOT NULL,
    category character varying(50) COLLATE pg_catalog."default" NOT NULL,
    type character varying(50) COLLATE pg_catalog."default" NOT NULL,
    brand character varying(50) COLLATE pg_catalog."default" NOT NULL,
    size character varying(20) COLLATE pg_catalog."default" NOT NULL,
    description text COLLATE pg_catalog."default",
    price numeric(10, 2) NOT NULL,
    image_url character varying COLLATE pg_catalog."default",
    CONSTRAINT products_pkey PRIMARY KEY (product_id)
);

CREATE TABLE IF NOT EXISTS public.product_warehouse
(
    product_warehouse_id integer NOT NULL,
    product_id integer,
    quantity integer,
    CONSTRAINT product_warehouse_pkey PRIMARY KEY (product_warehouse_id)
);

CREATE TABLE IF NOT EXISTS public.staffmembers
(
    staff_id serial NOT NULL,
    name character varying(100) COLLATE pg_catalog."default" NOT NULL,
    address character varying(255) COLLATE pg_catalog."default" NOT NULL,
    salary numeric(10, 2) NOT NULL,
    job_title character varying(100) COLLATE pg_catalog."default" NOT NULL,
    password character varying(255) COLLATE pg_catalog."default",
    CONSTRAINT staffmembers_pkey PRIMARY KEY (staff_id)
);

CREATE TABLE IF NOT EXISTS public.stock
(
    stock_id serial NOT NULL,
    product_id integer NOT NULL,
    warehouse_id integer NOT NULL,
    quantity integer NOT NULL,
    CONSTRAINT stock_pkey PRIMARY KEY (stock_id)
);

CREATE TABLE IF NOT EXISTS public.supplier
(
    supplier_id integer NOT NULL,
    supplier_name character varying COLLATE pg_catalog."default",
    address_id integer,
    CONSTRAINT supplier_pkey PRIMARY KEY (supplier_id)
);

CREATE TABLE IF NOT EXISTS public.supplier_product
(
    supplier_product_id integer NOT NULL,
    supplier_id integer,
    product_id integer,
    supplier_price numeric,
    CONSTRAINT supplier_product_pkey PRIMARY KEY (supplier_product_id)
);

CREATE TABLE IF NOT EXISTS public.users
(
    user_id serial NOT NULL,
    user_type character varying(20) COLLATE pg_catalog."default" NOT NULL,
    name character varying(100) COLLATE pg_catalog."default" NOT NULL,
    address character varying(255) COLLATE pg_catalog."default" NOT NULL,
    credit_card_number character varying(16) COLLATE pg_catalog."default",
    payment_address character varying(255) COLLATE pg_catalog."default",
    balance numeric(10, 2) DEFAULT 0,
    CONSTRAINT users_pkey PRIMARY KEY (user_id)
);

CREATE TABLE IF NOT EXISTS public.warehouses
(
    warehouse_id serial NOT NULL,
    address_id integer NOT NULL,
    warehouse_capacity integer,
    warehouse_name character varying COLLATE pg_catalog."default",
    CONSTRAINT warehouses_pkey PRIMARY KEY (warehouse_id)
);

ALTER TABLE IF EXISTS public.creditcards
    ADD CONSTRAINT creditcards_customer_id_fkey FOREIGN KEY (customer_id)
    REFERENCES public.customer (customer_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;
CREATE INDEX IF NOT EXISTS idx_credit_cards_customer_id
    ON public.creditcards(customer_id);


ALTER TABLE IF EXISTS public.creditcards
    ADD CONSTRAINT payment_address FOREIGN KEY (payment_address_id)
    REFERENCES public."Address" (address_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public.customer_address
    ADD CONSTRAINT customer_address_ref FOREIGN KEY (address_id)
    REFERENCES public."Address" (address_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public.customer_address
    ADD CONSTRAINT customer_addresses FOREIGN KEY (customer_id)
    REFERENCES public.customer (customer_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public.deliveryplans
    ADD CONSTRAINT deliveryplans_order_id_fkey FOREIGN KEY (order_id)
    REFERENCES public.orders (order_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;
CREATE INDEX IF NOT EXISTS idx_delivery_plans_order_id
    ON public.deliveryplans(order_id);


ALTER TABLE IF EXISTS public.orderitems
    ADD CONSTRAINT orderitems_order_id_fkey FOREIGN KEY (order_id)
    REFERENCES public.orders (order_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;
CREATE INDEX IF NOT EXISTS idx_order_items_order_id
    ON public.orderitems(order_id);


ALTER TABLE IF EXISTS public.orderitems
    ADD CONSTRAINT orderitems_product_id_fkey FOREIGN KEY (product_id)
    REFERENCES public.product (product_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.orders
    ADD CONSTRAINT customer_credit_card FOREIGN KEY (credit_card_id)
    REFERENCES public.creditcards (credit_card_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public.orders
    ADD CONSTRAINT orders_customer_id_fkey FOREIGN KEY (customer_id)
    REFERENCES public.users (user_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;
CREATE INDEX IF NOT EXISTS idx_order_customer_id
    ON public.orders(customer_id);


ALTER TABLE IF EXISTS public.product_warehouse
    ADD CONSTRAINT warehouse_products FOREIGN KEY (product_id)
    REFERENCES public.product (product_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.stock
    ADD CONSTRAINT stock_product_id_fkey FOREIGN KEY (product_id)
    REFERENCES public.product (product_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.stock
    ADD CONSTRAINT stock_warehouse_id_fkey FOREIGN KEY (warehouse_id)
    REFERENCES public.warehouses (warehouse_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.supplier
    ADD CONSTRAINT supplier_address FOREIGN KEY (address_id)
    REFERENCES public."Address" (address_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.supplier_product
    ADD CONSTRAINT product_ref FOREIGN KEY (product_id)
    REFERENCES public.product (product_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public.supplier_product
    ADD CONSTRAINT supplier_ref FOREIGN KEY (supplier_id)
    REFERENCES public.supplier (supplier_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;

END;