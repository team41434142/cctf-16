(ns shifty
  (:use clojure.repl))

(defn
  ^{:doc "Encrypts plaintext with shift cipher using random-length key."}
  shiftcipher [plaintext]
  (let [k (+ 1 (rand-int 25))]
    (->> plaintext
         .toUpperCase
         (map int)
         (filter #(<= 65 % 90))
         (map #(-> %
                   (+ k)
                   (- 65)
                   (mod 26)
                   (+ 65)
                   char))
         (apply str))))

;;Frequencies of characters in English alphabet
(def charfreqs {\A 0.08167 \B 0.01492 \C 0.02782 \D 0.04253 \E 0.12702 \F 0.02228 \G 0.02015 \H 0.06094 \I 0.06966 
  \J 0.00153 \K 0.00772 \L 0.04025 \M 0.02406 \N 0.06749 \O 0.07507 \P 0.01929 \Q 0.00095 \R 0.05987 \S 0.06327 \T 0.09056 
  \U 0.02758 \V 0.00978 \W 0.0236 \X 0.0015 \Y 0.01974 \Z 0.00074})

(def charfvals (vec (vals charfreqs)))

;;Used in shiftcracker to fill in missing values if ciphertext is lacking certain elements of the alphabet
(def zerofreqs (->> (range 65 91) (map char) (interpose 0) (into '(0)) (apply hash-map)))

(defn
  ^{:doc "Attempts to automatically produce the plaintext given a ciphertext encrypted with the shiftcipher fn.."}
  shiftcracker [ciphertext]
  (let [cipherfvals (->> ciphertext
                         frequencies
                         (mapcat (fn [x] [(first x) (/ (last x) (count ciphertext))]))
                         (apply hash-map)
                         (merge zerofreqs)
                         vals)
        keyval (inc
                (ffirst
                 (sort-by (fn [[x y]] y)
                          (map-indexed (fn [x y] [x (Math/abs (- 0.0655 y))])
                                       (for [xs (->>  cipherfvals
                                                      cycle
                                                      rest
                                                      (partition 26 1)
                                                      (take 25))]
                                         (reduce + (map * charfvals xs)))))))]
    (->> ciphertext
              (map #(-> %
                   int
                   (- 65)
                   (- keyval)
                   (mod 26)
                   (+ 65)
                   char))
              (apply str))))

;;"Lorem ipsum..." English translation example
(def loremipsum "But I must explain to you how all this mistaken idea of denouncing pleasure and praising pain was born 
  and I will give you a complete account of the system, and expound the actual teachings of the great explorer of the 
  truth, the master-builder of human happiness. No one rejects, dislikes, or avoids pleasure itself, because it is 
  pleasure, but because those who do not know how to pursue pleasure rationally encounter consequences that are extremely 
  painful. Nor again is there anyone who loves or pursues or desires to obtain pain of itself, because it is pain, but 
  because occasionally circumstances occur in which toil and pain can procure him some great pleasure. To take a trivial 
  example, which of us ever undertakes laborious physical exercise, except to obtain some advantage from it? But who has 
  any right to find fault with a man who chooses to enjoy a pleasure that has no annoying consequences, or one who avoids 
  a pain that produces no resultant pleasure?")

;;Try this
(def loremcipher (shiftcipher loremipsum))
(shiftcracker loremcipher)
